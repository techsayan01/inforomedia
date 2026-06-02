"""
SEO metadata generation — focus keyword, SEO title, meta description, tags,
LinkedIn hook, and pull quotes.

All functions are site-agnostic but tuned for entertainment industry content.
"""

from core.llm import call_llm
from core.retry import with_retry
from core.utils import log, safe_json_parse

_PERSONA_SEO = """\
You are an expert SEO and content strategist with 12 years optimising entertainment
industry trade publications — Variety, Deadline, Screen Daily, and similar outlets.
You write headlines and metadata that drive clicks from entertainment industry
professionals (acquisition execs, streaming strategists, distributors, financiers)
while accurately representing the article content.
You know exactly which headline formulas make an industry professional stop scrolling
and which ones get ignored. You never use clickbait that misrepresents the story.
"""

# ── Proven viral headline formulas for entertainment industry content ──────────
_HEADLINE_FORMULAS = """
Pick ONE of these proven formulas — choose whichever fits the story best:

1. THE REAL WINNER  — "Netflix Isn't the Real Winner of the Squid Game Deal"
2. NUMBER + REVEAL  — "The $200M Question Nobody's Asking About the Disney Merger"
3. INSIDER REFRAME  — "What the Deadline Report on BTS Actually Means for K-Pop Licensing"
4. SURPRISING LOSER — "Why Cannes' Biggest Winner Could Be Its Own Worst Deal"
5. EVERYONE'S WRONG — "The Box Office Narrative on Pathaan Is Completely Backwards"
6. HIDDEN IMPLICATION — "That Netflix Cancellation Reveals a Much Bigger Problem"
7. VS. FRAMING      — "Bollywood vs. Hollywood OTT: The Numbers Tell a Different Story"
8. TIME PRESSURE    — "The 90-Day Window That Will Decide K-Drama's Global Future"
9. WHAT THEY WON'T SAY — "What Nobody in Hollywood Is Saying About the Writers' Strike Data"
10. COUNTERINTUITIVE — "The Worst-Reviewed Film of Cannes Is Now Its Biggest Acquisition"

Rules:
- Under 65 characters total
- Must be accurate — do NOT misrepresent the story
- Use a specific name, number, or entity from the story when possible
- Do NOT use generic power words like "shocking", "amazing", "incredible"
- Industry professionals hate hyperbole — be sharp, not loud
"""


@with_retry(max_retries=2, delay=3, fallback=lambda: "")
def generate_focus_keyword(headline: str, category_name: str) -> str:
    """Extract the best 2–4 word SEO focus keyword from the headline."""
    return call_llm("gemini-2.5-flash", 30, [{"role": "user", "content": (
        f"{_PERSONA_SEO}\n\n"
        f"Extract the single best 2–4 word SEO focus keyword from this headline "
        f"for the '{category_name}' entertainment section.\n"
        f"Headline: {headline}\n"
        f"Rules:\n"
        f"- Choose the phrase an industry professional would search for\n"
        f"- Prefer specific terms over generic ones (e.g. 'netflix subscriber churn' over 'streaming news')\n"
        f"- Lowercase, no quotes, no punctuation\n"
        f"Return ONLY the keyword phrase."
    )}]).strip().lower()


@with_retry(max_retries=2, delay=3, fallback=lambda: "Untitled Article")
def generate_seo_title(headline: str, market_trend: str) -> str:
    """Generate a viral, opinionated SEO headline using proven entertainment formulas."""
    return call_llm("gemini-2.5-flash", 150, [{"role": "user", "content": (
        f"{_PERSONA_SEO}\n\n"
        f"Write ONE headline for this entertainment industry story.\n\n"
        f"{_HEADLINE_FORMULAS}\n"
        f"Original headline: {headline}\n"
        f"Market trend: {market_trend}\n\n"
        f"Return ONLY the headline, no quotes, no explanation."
    )}]).strip()


@with_retry(max_retries=2, delay=3, fallback=lambda: "")
def generate_meta_description(title: str, content: str, focus_keyword: str) -> str:
    """Generate a 150–155 character meta description with the focus keyword."""
    log.info("  📝 Generating meta description…")
    desc = call_llm("gemini-2.5-flash", 100, [{"role": "user", "content": (
        f"{_PERSONA_SEO}\n\n"
        f"Write a meta description of EXACTLY 150–155 characters for this entertainment article.\n"
        f"Must include the keyword '{focus_keyword}' naturally.\n"
        f"Must hint at the insider angle — make the reader feel they'll learn something "
        f"they can't get from Deadline or Variety.\n"
        f"End with a subtle call-to-action.\n"
        f"Title: {title}\n"
        f"Return ONLY the meta description — no quotes, no labels."
    )}]).strip()
    if len(desc) > 160:
        desc = desc[:157] + "..."
    return desc


@with_retry(max_retries=2, delay=3, fallback=list)
def generate_tags(
    headline: str,
    focus_keyword: str,
    market_trend: str,
    named_entities: list[str] | None = None,
) -> list[str]:
    """Generate 6–10 WordPress tags for the article."""
    entities_hint = ""
    if named_entities:
        entities_hint = (
            f"Named entities: {', '.join(named_entities[:8])}. "
            f"Include the most prominent ones as tags."
        )

    raw = call_llm("gemini-2.5-flash", 150, [{"role": "user", "content": (
        f"{_PERSONA_SEO}\n\n"
        f"Generate 6–10 WordPress tags for this entertainment industry article.\n"
        f"Headline: {headline}\n"
        f"Focus keyword: {focus_keyword}\n"
        f"Market trend: {market_trend}\n"
        f"{entities_hint}\n\n"
        f"Rules:\n"
        f"- Specific and searchable (e.g. 'netflix subscriber data', 'cannes acquisition', 'bts licensing deal')\n"
        f"- Include the focus keyword and market trend as tags\n"
        f"- Include relevant platform names, studio names, or artist names\n"
        f"- All lowercase, no special characters\n"
        f"- No generic tags like 'news', 'entertainment', 'article', 'hollywood news'\n"
        f"Return ONLY a JSON array: [\"tag1\", \"tag2\", ...]"
    )}])

    tags = safe_json_parse(raw)
    if isinstance(tags, list):
        return [str(t).lower().strip() for t in tags if t][:10]
    return []


@with_retry(max_retries=2, delay=3, fallback=lambda: "")
def generate_linkedin_hook(title: str, viral_angle: str, focus_keyword: str) -> str:
    """Generate a 2-line LinkedIn hook optimised for the pre-truncation window.

    LinkedIn shows ~2 lines before 'See more'. These 2 lines determine whether
    industry professionals click. Returns a newline-separated 2-line string.
    """
    raw = call_llm("gemini-2.5-flash", 120, [{"role": "user", "content": (
        f"{_PERSONA_SEO}\n\n"
        f"Write a 2-line LinkedIn hook for an entertainment industry article.\n\n"
        f"Article title: {title}\n"
        f"Key insight: {viral_angle}\n"
        f"Focus keyword: {focus_keyword}\n\n"
        f"Rules:\n"
        f"Line 1: A provocative claim, surprising number, or counterintuitive statement "
        f"(max 140 characters). Make a content acquisition exec stop scrolling.\n"
        f"Line 2: The stakes — why this matters RIGHT NOW for the industry "
        f"(max 140 characters). No fluff.\n\n"
        f"Do NOT use emojis. Do NOT use hashtags. Do NOT use 'I' or 'We'.\n"
        f"Format: LINE1\\nLINE2\n"
        f"Return ONLY the two lines."
    )}]).strip()
    return raw


@with_retry(max_retries=2, delay=3, fallback=list)
def generate_pull_quotes(
    headline: str,
    viral_angle: str,
    key_figures: list[str],
) -> list[str]:
    """Generate 2 pull quotes designed to be screenshot and shared.

    Each quote must be a standalone insight — someone reading only the pull quote
    must understand the point without reading the full article.
    Returns a list of 2 quote strings.
    """
    figures_hint = f"Key figures: {', '.join(key_figures[:5])}" if key_figures else ""

    raw = call_llm("gemini-2.5-flash", 200, [{"role": "user", "content": (
        f"{_PERSONA_SEO}\n\n"
        f"Write 2 pull quotes for this entertainment industry article.\n\n"
        f"Headline: {headline}\n"
        f"Key insight: {viral_angle}\n"
        f"{figures_hint}\n\n"
        f"Rules:\n"
        f"- Each quote is 20–35 words — punchy, self-contained, shareable\n"
        f"- Quote 1: A counterintuitive or surprising industry insight\n"
        f"- Quote 2: A specific data point or implication with business stakes\n"
        f"- Must read as a standalone thought — no 'this' or 'it' without context\n"
        f"- Write as editorial voice, not as a quote from a named person\n"
        f"- Do NOT fabricate numbers not in the source material\n\n"
        f"Return ONLY a JSON array of 2 strings: [\"quote1\", \"quote2\"]"
    )}])

    quotes = safe_json_parse(raw)
    if isinstance(quotes, list) and len(quotes) >= 2:
        return [str(q).strip() for q in quotes[:2]]
    return []
