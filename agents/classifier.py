"""
Agent 0 — Article Type Classifier.

Classifies a story into one of the site's registered article types so the
writer can pick the appropriate template. Uses a fast Gemini Flash call.

Default types (GrowStream / fintech):
  breaking_news   — default catch-all for hard news
  data_insights   — surveys, research, benchmark reports
  earnings        — quarterly results, revenue announcements
  product_launch  — new tools, platform updates, feature releases
  funding         — investment rounds, M&A, IPOs
  regulatory      — fines, enforcement, compliance actions
  market_movers   — macro moves, index/stock movements
  explainer       — educational, "what is X", how-to guides

Sites override the type set via agents.personas.configure(article_types={...}).
"""

from agents.personas import get_article_types as _get_article_types
from core.llm import call_llm
from core.utils import log, safe_json_parse

# ── Default article types (GrowStream / fintech) ──────────────────────────────
DEFAULT_ARTICLE_TYPES: dict[str, str] = {
    "breaking_news":  "Hard news, announcements, incidents — default when nothing else fits",
    "data_insights":  "Survey results, research reports, statistics, benchmark studies",
    "earnings":       "Quarterly results, revenue, profit, EPS, guidance",
    "product_launch": "New product, feature, platform, tool, or service announcement",
    "funding":        "Investment round, M&A deal, acquisition, IPO, valuation",
    "regulatory":     "Fine, enforcement action, compliance ruling, regulatory guidance",
    "market_movers":  "Stock/index movement, macro event, Fed/central bank action",
    "explainer":      "Educational piece, 'what is X', how-to, concept guide",
}

_PROMPT_TMPL = """\
You are an experienced news editor. Classify the following story into exactly one article type.

Article types:
{type_list}

Story headline: {headline}
Story summary: {summary}

Return ONLY this JSON (no markdown, no explanation):
{{"type": "<one of the types above>", "confidence": 0.9}}
"""


def classify_story(story: dict) -> str:
    """Return the article type string for *story*. Falls back to 'breaking_news'."""
    # Use site-configured types if set, otherwise fall back to defaults
    configured = _get_article_types()
    if configured:
        # configured is a set[str] — build description map from known defaults + unknowns
        type_map = {k: v for k, v in DEFAULT_ARTICLE_TYPES.items() if k in configured}
        for t in configured:
            if t not in type_map:
                type_map[t] = "Classify here when no other type fits better"
    else:
        type_map = DEFAULT_ARTICLE_TYPES

    type_list = "\n".join(f"- {k}: {v}" for k, v in type_map.items())
    valid_types = set(type_map.keys())

    headline = story.get("headline", "")
    summary  = story.get("summary", "")[:400]

    prompt = _PROMPT_TMPL.format(
        type_list=type_list,
        headline=headline,
        summary=summary,
    )
    try:
        raw    = call_llm("gemini-2.5-flash", 60, [{"role": "user", "content": prompt}])
        result = safe_json_parse(raw)
        if result and isinstance(result, dict):
            article_type = result.get("type", "breaking_news")
            if article_type in valid_types:
                confidence = result.get("confidence", 0)
                log.info(f"  🏷  Article type: {article_type} (confidence: {confidence})")
                return article_type
    except Exception as e:
        log.warning(f"  ⚠ Classifier failed: {e} — defaulting to breaking_news")

    return "breaking_news"
