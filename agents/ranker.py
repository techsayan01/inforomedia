"""
Agent 2 — Story Ranking (Dr. Sarah Chen, Chief Market Intelligence Analyst).

Scores stories on RELEVANCE TO AUDIENCE and EDITORIAL FIT, then combines
with pre-computed freshness and source-reputation signals into a composite
score. Returns the top 3 stories ordered by composite score.

Virality is intentionally removed — we have no engagement data to base it
on and LLM-hallucinated virality scores produced noise, not signal.
"""

import json

from agents.personas import get_persona as _get_persona, get_trend_alignment as _get_trend_alignment
from core.llm import call_llm
from core.retry import with_retry
from core.utils import log, safe_json_parse

_DEFAULT_PERSONA = """\
You are Dr. Sarah Chen, Chief Market Intelligence Analyst at GrowStream Media.
Background: CFA charterholder, 18 years in institutional finance and financial media.
You evaluate news through the lens of its impact on institutional investors,
CFOs, and finance operations leaders.
You are ruthless about relevance — a story must move markets, change behaviour,
or signal a structural shift to merit coverage.
Zero patience for PR fluff, incremental product updates, or hype without data.
"""

_DEFAULT_TREND_ALIGNMENT = [
    "AI Infrastructure Boom", "Fintech Disruption", "Regulatory Crackdown",
    "Investment AI", "Banking Transformation", "Payments Evolution",
]

_DEFAULT_SCORING_PROMPT = """\
Scoring dimensions (each 1–10):

1. AUDIENCE RELEVANCE — how directly does this story affect CFOs, institutional
   investors, or finance ops leaders? Requires specific impact, not just vague
   connection to finance. A story about "AI productivity" scores low; a story
   about "Goldman Sachs cutting 200 compliance roles to AI automation" scores high.

2. EDITORIAL FIT — does this story give the writer enough material to produce a
   strong, substantive article? Data-rich, named-source stories score high.
   Single-sentence press releases with no figures score low.

3. MACRO TREND ALIGNMENT — does it map to one of these structural shifts?
   {trends}"""

# Composite score weights
_W_RELEVANCE  = 0.30
_W_FRESHNESS  = 0.20
_W_SOURCE     = 0.10
_W_VIRALITY   = 0.20
_W_FIT        = 0.20


@with_retry(max_retries=3, delay=5)
def rank_stories(stories: list[dict], category: dict) -> list[dict] | None:
    """Score stories and return the top 3 by composite score."""
    persona       = _get_persona("ranker") or _DEFAULT_PERSONA
    trends        = _get_trend_alignment() or _DEFAULT_TREND_ALIGNMENT
    trends_str    = " | ".join(trends)
    scoring_block = _DEFAULT_SCORING_PROMPT.format(trends=trends_str)
    site_name     = category.get("site_display_name", "our publication")

    log.info(
        f"📊 [Agent 2 — Ranker] Ranking {len(stories)} stories "
        f"for {category['name']}"
    )

    stories_json = json.dumps(
        [
            {
                "index":    i,
                "headline": s["headline"],
                "summary":  s["summary"][:600],
                "source":   s["source"],
                "age":      s.get("age_label", "unknown"),
            }
            for i, s in enumerate(stories)
        ],
        indent=2,
    )

    prompt = f"""{persona}

Score each story for the '{category['name']}' section of {site_name}.

{scoring_block}

Stories:
{stories_json}

Return ONLY this JSON (no markdown):
{{
  "scores": [
    {{
      "index": 0,
      "audience_relevance": 8,
      "editorial_fit": 7,
      "macro_trend": "{trends[0]}",
      "rationale": "One sentence — why this story matters to the target audience.",
      "key_facts": ["Concrete fact 1 from the text", "Concrete fact 2", "Concrete fact 3"]
    }}
  ]
}}

Rules:
- Score every story in the input — one entry per index.
- key_facts must be extracted verbatim or closely paraphrased from the story text — do NOT invent figures.
- If a story has no concrete data (no figures, no named entities), cap editorial_fit at 4.
"""

    raw    = call_llm("gemini-2.5-flash", 2000, [{"role": "user", "content": prompt}])
    result = safe_json_parse(raw)

    if not result or "scores" not in result:
        raise ValueError("Ranking response missing 'scores' key")

    score_map: dict[int, dict] = {}
    for item in result["scores"]:
        idx = item.get("index")
        if idx is None or not isinstance(idx, int):
            continue
        score_map[idx] = item

    # Build enriched stories with composite score
    enriched: list[dict] = []
    for i, story in enumerate(stories):
        llm_scores = score_map.get(i, {})
        relevance  = float(llm_scores.get("audience_relevance", 5))
        fit        = float(llm_scores.get("editorial_fit", 5))
        freshness  = float(story.get("freshness_score", 5))
        source_rep = float(story.get("source_score", 5))
        virality   = float(story.get("virality_signal", 5))

        composite = (
            relevance  * _W_RELEVANCE +
            fit        * _W_FIT +
            freshness  * _W_FRESHNESS +
            source_rep * _W_SOURCE +
            virality   * _W_VIRALITY
        )

        enriched.append({
            **story,
            "market_trend":           llm_scores.get("macro_trend", ""),
            "market_relevance_score": round(relevance, 1),
            "editorial_fit_score":    round(fit, 1),
            "virality_score":         round(virality, 1),
            "composite_score":        round(composite, 2),
            "ranking_rationale":      llm_scores.get("rationale", ""),
            "key_facts":              llm_scores.get("key_facts", []),
        })

    # Sort by composite score and return top 3
    enriched.sort(key=lambda s: s["composite_score"], reverse=True)
    top = enriched[:3]

    for rank, s in enumerate(top, 1):
        log.info(
            f"  #{rank} [{s['composite_score']:.1f}] "
            f"Rel:{s['market_relevance_score']} Fit:{s['editorial_fit_score']} "
            f"Fresh:{s['freshness_score']} Src:{s['source_score']} "
            f"Viral:{s['virality_score']} "
            f"| {s['headline'][:50]}"
        )

    return top
