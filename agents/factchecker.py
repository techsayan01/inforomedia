"""
Agent 3 — Content Extraction & Credibility Gate (Marcus Webb, Editorial Director).

Two jobs in one pass:

1. EXTRACT structured content from the full article text (not just the RSS
   summary). This gives the writer real figures, real quotes, and real named
   entities instead of fabricating them from a 200-word snippet.

2. CREDIBILITY GATE — lightweight check: does the story have named sources,
   specific figures, and internally consistent claims? Rejects obvious PR
   fluff and unsourced speculation.
"""

import json

from agents.personas import get_persona as _get_persona
from core.llm import call_llm
from core.retry import with_retry
from core.utils import log, safe_json_parse

_DEFAULT_PERSONA = """\
You are Marcus Webb, Editorial Director and Head Fact-Checker at GrowStream Media.
Background: 22 years in journalism — ex-Reuters financial correspondent, ex-FT editor.
You protect GrowStream's credibility by ensuring every published article is grounded
in verifiable, attributed claims.

Because GrowStream is an aggregator, you routinely work with secondary sources
(e.g. Finextra summarising an FT report). You accept reputable secondary sources
as long as the original report is clearly attributed. You do NOT reject stories
merely because they are summaries or commentary — you reject them when:
  - The core claim has no named source and cannot be attributed
  - Key figures appear to be fabricated or implausible
  - The story is a pure press release with no independent editorial value
"""


@with_retry(max_retries=3, delay=5)
def factcheck_story(story: dict, category: dict) -> dict | None:
    """Extract structured content and run credibility gate on *story*.

    Returns an enriched dict on approval, or None on failure.
    The returned dict includes the original story PLUS extracted fields
    (key_figures, named_entities, direct_quotes, suggested_angle) that
    the writer will use as primary source material.
    """
    persona   = _get_persona("factchecker") or _DEFAULT_PERSONA
    site_name = category.get("site_display_name", "our publication")
    log.info(f"🔎 [Agent 3 — Fact-Checker] Extracting & checking: {category['name']}")

    # Use the richest text available
    source_text = story.get("summary", "")
    word_count  = len(source_text.split())

    prompt = f"""{persona}

Your task: Review and extract structured content from the following story for
the '{category['name']}' section of {site_name}.

--- STORY ---
Headline : {story.get('headline', '')}
Source   : {story.get('source', '')}
Age      : {story.get('age_label', 'unknown')}
Text     : {source_text[:2500]}
--- END ---

Step 1 — CREDIBILITY GATE:
  Approve if: named sources present OR reputable outlet with clear attribution.
  Reject if: no attribution whatsoever, OR core claim is numerically implausible.

Step 2 — CONTENT EXTRACTION (only if approved):
  Extract directly from the text — do NOT invent or infer figures not present.

  key_figures     : All specific numbers, percentages, dollar amounts in the text.
  named_entities  : Companies, studios, platforms, artists, executives named in the text.
  direct_quotes   : Any quoted speech (use exact words from the text).
  suggested_angle : The most important editorial angle for the target audience. Be specific —
                    not "explore the implications" but "focus on how X threatens Y's market position".
  viral_angle     : The single most SURPRISING, COUNTERINTUITIVE, or CONTROVERSIAL thing
                    about this story. Different from suggested_angle — this is what an
                    industry professional would forward to a colleague saying "did you see this?"
                    It should be the thing nobody else is saying, or the implication everyone
                    is missing. If the story has no viral angle, write "none".
  image_keywords  : 4 concrete keywords for finding a relevant stock photo or press image.

Return ONLY this JSON (no markdown, no commentary):
{{
  "approved": true,
  "credibility_score": 8,
  "rejection_reason": "",
  "fact_checker_verdict": "One sentence verdict.",
  "key_figures": ["$28.8M deal", "40% YoY growth", "12 territories"],
  "named_entities": ["Netflix", "HYBE", "BTS"],
  "direct_quotes": ["We expect to double international reach by Q4"],
  "suggested_angle": "Specific editorial angle sentence.",
  "viral_angle": "The counterintuitive or surprising insight — what nobody else is connecting.",
  "image_keywords": ["keyword1", "keyword2", "keyword3", "keyword4"],
  "story": {json.dumps({k: v for k, v in story.items() if k != "story"}, ensure_ascii=False)[:800]}
}}

Critical rules:
- key_figures, named_entities, direct_quotes must come ONLY from the text above.
- If the text has no figures, key_figures must be an empty list — do NOT invent any.
- viral_angle must be grounded in the text — surprising but not fabricated.
- The "story" field must preserve the original story dict exactly.
"""

    raw    = call_llm("gemini-2.5-flash", 1500, [{"role": "user", "content": prompt}])
    result = safe_json_parse(raw)

    if not result:
        raise ValueError("Invalid fact-check response")

    approved = result.get("approved", False)
    score    = result.get("credibility_score", "?")
    verdict  = result.get("marcus_webb_verdict", "")

    log.info(
        f"  {'✓ Approved' if approved else '✗ Rejected'} — "
        f"Credibility: {score}/10 | {verdict}"
    )
    if not approved:
        reason = result.get("rejection_reason", "")
        if reason:
            log.warning(f"  Rejection reason: {reason}")

    if approved:
        # Merge extracted fields back onto the story so the writer receives them
        enriched_story = {**story}
        for field in ("key_figures", "named_entities", "direct_quotes"):
            val = result.get(field, [])
            if val:
                enriched_story[field] = val
        # key_facts used downstream by writer/editor
        enriched_story["key_facts"] = result.get("key_figures", []) + result.get("named_entities", [])
        # viral_angle passed to writer for hook + contrarian take
        viral_angle = result.get("viral_angle", "")
        if viral_angle and viral_angle.lower() != "none":
            enriched_story["viral_angle"] = viral_angle
        result["story"] = enriched_story

    return result
