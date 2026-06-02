"""
Agent 1.5 — Virality Signal Enricher.

Runs between the Researcher and the Ranker. Takes stories with extracted
named_entities and attaches real-world engagement signals so the Ranker
can weight virality from actual data rather than LLM guesses.

Three signal sources (all free, no paid API keys required):

  1. Google Trends (pytrends)
       — search volume spike for named entities over the last 24h vs. 7-day baseline
       — returns a spike ratio: 2.0 = double normal volume, 10.0 = massive spike

  2. Wikipedia Pageviews API
       — daily page views for each named entity's Wikipedia page
       — spike ratio: today vs. 30-day rolling average
       — pure demand signal: people only look up Wikipedia when something happened

  3. Reddit Rising
       — upvote velocity on category-relevant subreddits within the last 6 hours
       — post score as proxy for community engagement heat

All three are combined into a single `virality_signal` score (0–10) per story.
Stories with no signal data get a neutral score of 5.0.

Failure modes are all soft — if any source is unavailable, it is skipped
and the remaining sources are weighted up. The pipeline never blocks on this.
"""

from __future__ import annotations

import re
import time
from datetime import datetime, timedelta, timezone

import requests

from core.utils import log

# ── Reddit subreddit map by category slug ─────────────────────────────────────
_REDDIT_SUBS: dict[str, list[str]] = {
    "hollywood":       ["movies", "boxoffice", "flicks"],
    "bollywood":       ["bollywood", "indiancinema"],
    "kdrama-kpop":     ["kdrama", "kpop", "koreanvariety"],
    "japanese-anime":  ["anime", "animenews", "japanesefilm"],
    "chinese-cinema":  ["cdrama", "chinesedrama", "asiancinema"],
    "world-cinema":    ["worldcinema", "flicks", "TrueFilm"],
    "streaming-wars":  ["netflix", "cordcutters", "DisneyPlus"],
    "awards-festivals":["oscarrace", "movies", "flicks"],
    # GrowStream fallback
    "default":         ["technology", "business"],
}

_WIKI_API   = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article"
_REDDIT_API = "https://www.reddit.com/r/{sub}/rising.json"
_REQUEST_HEADERS = {"User-Agent": "InfoRoMediaBot/1.0 (editorial signal enricher)"}
_TIMEOUT = 6  # seconds per HTTP call


# ── Helpers ───────────────────────────────────────────────────────────────────

def _clean_entity(entity: str) -> str:
    """Normalise an entity name for API lookups."""
    return re.sub(r"\s+", "_", entity.strip().title())


def _safe_get(url: str, params: dict | None = None) -> dict | None:
    try:
        r = requests.get(url, params=params, headers=_REQUEST_HEADERS, timeout=_TIMEOUT)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None


# ── Signal 1: Google Trends ───────────────────────────────────────────────────

def _google_trends_spike(entities: list[str]) -> float:
    """Return a spike ratio 0–10 for the top entity using pytrends.

    Compares the last data point (most recent hour/day) against the
    7-day average. Capped at 10.0.
    """
    if not entities:
        return 5.0
    try:
        from pytrends.request import TrendReq
        pt = TrendReq(hl="en-US", tz=0, timeout=(4, 8), retries=1, backoff_factor=0.5)
        # Use only the top 1–2 entities to stay within pytrends limits
        kw_list = [e.replace("_", " ") for e in entities[:2]]
        pt.build_payload(kw_list, timeframe="now 7-d", geo="")
        df = pt.interest_over_time()
        if df.empty:
            return 5.0

        col = kw_list[0]
        if col not in df.columns:
            return 5.0

        series   = df[col].dropna()
        if len(series) < 2:
            return 5.0

        baseline = float(series[:-6].mean()) if len(series) > 6 else float(series.mean())
        recent   = float(series[-3:].mean())  # last ~3 hours

        if baseline < 1:
            return 5.0  # no meaningful data

        ratio = recent / baseline
        # Map: 1.0 = neutral (5), 3.0 = strong (8), 5.0+ = massive (10)
        score = min(10.0, 3.0 + (ratio - 1.0) * 2.5)
        return round(max(0.0, score), 1)

    except Exception as e:
        log.debug(f"    Google Trends unavailable: {e}")
        return 5.0


# ── Signal 2: Wikipedia Pageviews ─────────────────────────────────────────────

def _wikipedia_spike(entities: list[str]) -> float:
    """Return a spike ratio 0–10 based on Wikipedia pageview anomaly.

    Compares today's views against the 30-day rolling average for the
    most prominent named entity in the story.
    """
    today     = datetime.now(timezone.utc)
    yesterday = today - timedelta(days=1)
    month_ago = today - timedelta(days=30)

    date_fmt  = "%Y%m%d"
    today_str = yesterday.strftime(date_fmt)   # yesterday = last complete day
    start_str = month_ago.strftime(date_fmt)

    best_score = 5.0

    for entity in entities[:3]:
        page = _clean_entity(entity)
        url  = (
            f"{_WIKI_API}/en.wikipedia/all-access/all-agents"
            f"/{page}/daily/{start_str}/{today_str}"
        )
        data = _safe_get(url)
        if not data or "items" not in data:
            continue

        views = [item["views"] for item in data["items"] if "views" in item]
        if len(views) < 7:
            continue

        baseline = sum(views[:-1]) / max(len(views) - 1, 1)
        recent   = views[-1]

        if baseline < 100:
            continue  # page too obscure to be meaningful

        ratio = recent / baseline
        # 1.0 = neutral (5), 5.0 = strong (8), 20.0+ = massive (10)
        score = min(10.0, 3.0 + (ratio - 1.0) * 0.7)
        score = round(max(0.0, score), 1)

        log.debug(f"    Wikipedia [{page}]: {recent:,} views vs {baseline:,.0f} avg → spike {ratio:.1f}x → {score}")
        best_score = max(best_score, score)

    return best_score


# ── Signal 3: Reddit Rising ───────────────────────────────────────────────────

def _reddit_rising(entities: list[str], category_slug: str) -> float:
    """Return a score 0–10 based on upvote velocity in relevant subreddits.

    Checks rising posts in category-relevant subs. If any post title
    overlaps with the story entities → score based on upvote count.
    """
    subs = _REDDIT_SUBS.get(category_slug, _REDDIT_SUBS["default"])
    entity_tokens = {t.lower() for e in entities for t in e.split()}

    best_score = 0.0

    for sub in subs[:2]:  # max 2 subs to avoid rate limits
        url  = _REDDIT_API.format(sub=sub)
        data = _safe_get(url)
        if not data:
            continue

        posts = data.get("data", {}).get("children", [])
        for post in posts[:25]:
            pdata  = post.get("data", {})
            title  = pdata.get("title", "").lower()
            score  = pdata.get("score", 0)
            upvote = pdata.get("upvote_ratio", 0.5)

            title_tokens = set(re.findall(r"\b\w{3,}\b", title))
            overlap = len(entity_tokens & title_tokens)

            if overlap >= 1:
                # Score: 100 upvotes = 4, 500 = 6, 2000 = 8, 5000+ = 10
                raw = min(10.0, 3.0 + (score ** 0.4) * 0.35)
                raw = round(raw * upvote, 1)  # penalise low upvote ratio
                log.debug(f"    Reddit r/{sub}: '{title[:50]}' score={score} → {raw}")
                best_score = max(best_score, raw)

        time.sleep(0.5)  # be polite to Reddit

    return round(best_score, 1) if best_score > 0 else 5.0


# ── Composite virality score ──────────────────────────────────────────────────

def _composite_virality(
    trends_score:  float,
    wiki_score:    float,
    reddit_score:  float,
) -> float:
    """Combine three signals into one 0–10 virality score.

    Weights reflect reliability: Wikipedia is most trustworthy (pure demand),
    Reddit is most real-time, Google Trends is broadest but noisiest.
    """
    # Skip any source that returned exactly 5.0 (neutral/unavailable)
    # to avoid dragging down genuinely spiking scores
    sources = []
    if trends_score != 5.0:
        sources.append((trends_score, 0.30))
    if wiki_score != 5.0:
        sources.append((wiki_score,   0.45))
    if reddit_score != 5.0:
        sources.append((reddit_score, 0.25))

    if not sources:
        return 5.0

    total_weight = sum(w for _, w in sources)
    score = sum(s * w for s, w in sources) / total_weight
    return round(min(10.0, max(0.0, score)), 1)


# ── Public interface ──────────────────────────────────────────────────────────

def enrich_with_signals(stories: list[dict], category: dict) -> list[dict]:
    """Attach virality_signal score to each story in-place and return the list.

    Named entities come from the researcher's story dict. If not present,
    the story headline tokens are used as a fallback.

    All errors are soft — a story always gets a score, even if all sources fail.
    """
    slug = category.get("slug", "default")
    log.info(f"📡 [Agent 1.5 — Signal Enricher] Scoring {len(stories)} stories for {category['name']}")

    for story in stories:
        entities = story.get("named_entities") or story.get("key_facts") or []
        if not entities:
            # Fall back to capitalised tokens from headline
            entities = re.findall(r"\b[A-Z][a-zA-Z]{2,}\b", story.get("headline", ""))

        if not entities:
            story["virality_signal"]  = 5.0
            story["virality_sources"] = {}
            continue

        trends = _google_trends_spike(entities)
        wiki   = _wikipedia_spike(entities)
        reddit = _reddit_rising(entities, slug)
        score  = _composite_virality(trends, wiki, reddit)

        story["virality_signal"]  = score
        story["virality_sources"] = {
            "google_trends": trends,
            "wikipedia":     wiki,
            "reddit":        reddit,
        }
        log.info(
            f"  📊 '{story['headline'][:45]}' → "
            f"Trends:{trends} Wiki:{wiki} Reddit:{reddit} → Viral:{score}"
        )

    return stories
