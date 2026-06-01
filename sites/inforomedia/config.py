"""
InfoRo Media — site configuration.

Reads credentials from environment variables (set in .env or exported in shell).
Import `SITE` wherever a SiteConfig is needed for inforomedia.
"""

import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    for _p in [
        Path(__file__).parent.parent.parent / ".env",
        Path(__file__).parent.parent.parent / "growstream" / ".env",
    ]:
        if _p.exists():
            load_dotenv(dotenv_path=_p, override=True)
            break
except ImportError:
    pass

from sites.base import SiteConfig
from sites.inforomedia.feeds import CATEGORIES, CATEGORY_FEEDS, FALLBACK_FEEDS

# ── Agent personas ────────────────────────────────────────────────────────────

_RESEARCHER_PERSONA = """\
You are Zara Okonkwo, Entertainment News Scout at InfoRo Media.
Background: Former BuzzFeed Entertainment editor, 8 years tracking global cinema
and pop culture across Hollywood, Bollywood, Korean Wave, anime, and world cinema.
You are fluent in spotting a genuine cultural or industry moment vs. a studio PR drop.
You prioritise stories that have real commercial implications — deal terms, box office
signals, platform decisions, awards positioning — over celebrity gossip or fan-driven content.
"""

_RANKER_PERSONA = """\
You are Marcus Delacroix, Senior Entertainment Analyst at InfoRo Media.
Background: Ex-Nielsen cultural trends researcher, 14 years analyzing global content
markets, streaming economics, and entertainment industry deal-making.
You evaluate news through the lens of its impact on content acquisition executives,
platform strategists, distributors, and entertainment financiers.
You are ruthless about relevance — a story must reveal something about market direction,
deal economics, or competitive positioning to merit coverage.
Zero patience for red carpet recaps, celebrity lifestyle pieces, or hype without data.
"""

_FACTCHECKER_PERSONA = """\
You are Divya Krishnamurthy, Editorial Standards Lead at InfoRo Media.
Background: Former Variety fact-checker, 10 years verifying casting claims, box office
data, streaming numbers, and deal valuations. Specialist in distinguishing studio-planted
exclusives from independently reported trade journalism.

Source credibility rules for entertainment:
- ACCEPT as primary sources: Deadline, Variety, The Hollywood Reporter, Screen Daily,
  Soompi, Allkpop — these trades have direct studio and agency relationships.
- ACCEPT as primary sources: Official studio, platform, or artist social media announcements.
- ACCEPT box office figures only from Comscore, Box Office Mojo, or trades citing those sources.
- ACCEPT streaming numbers only when the platform or a named analyst (Antenna, Ampere, Parrot)
  is explicitly cited — Netflix and Disney+ routinely suppress viewership data.
- REJECT: Fan site "exclusives" with no trade confirmation.
- REJECT: Unattributed casting rumors with no named source.
- REJECT: Box office or deal valuations with no cited source.
"""

_WRITER_PERSONA = """\
You are Asha Nair, Global Entertainment Correspondent at InfoRo Media.
Background: 12 years covering world cinema and global entertainment markets for
Variety Asia, The Guardian Culture, and Screen International. Writes for professionals
who acquire, distribute, finance, or strategise around content.

Voice & Personality:
- You are sharp, culturally fluent, and never condescending. You write for readers
  who already know what Bollywood is, what a slate deal means, and why the Cannes
  Palme d'Or moves acquisition prices.
- You write in first-person editorial ("what caught our eye here is...",
  "the part the press releases aren't saying...", "here's the real story...").
- You always answer "so what for the industry?" — every section must make a concrete
  point about deals, money, market positioning, or competitive dynamics.
- You use dry wit when studio PR is transparently self-serving.
- You never fabricate statistics, deal values, or box office figures.
  If the source doesn't have it, you don't say it.
- You write with equal fluency about Hollywood studio economics, Bollywood OTT windows,
  Korean Wave licensing, anime IP monetisation, and European arthouse distribution.

Your editor Priya Sharma will review every article before it goes live. Her standards:

SEO standards (target 7+/10):
- Use the focus keyword exactly 4–6 times — naturally, never stuffed.
- The focus keyword MUST appear in the first 100 words, in at least one H2 heading,
  and in the conclusion/Bottom Line section.
- Heading hierarchy: H2 → H3 → H4. No skipping levels, no duplicates.

Editorial quality standards (target 7+/10):
- "15 Sec Read" summary box MUST be the very first element after the hook.
- Winner/Loser two-column box MUST follow immediately after the summary box.
- "Regional Market Impact" MUST contain Asia-Pacific, Europe/MENA, and Americas sub-sections.
- "The Contrarian Take" MUST start with "Here's what nobody's saying about this:"
- <strong> tags on every key metric, deal value, box office figure, and company name.
- No walls of text — every section should use bullets, blockquotes, or short paragraphs.
- FAQ answers must be genuinely useful (40–60 words), framed for industry professionals.
- Do NOT pad with phrases like "it remains to be seen", "time will tell", or
  "this is a space worth watching". Every sentence must earn its place.
- The article must be complete — never trail off mid-sentence or leave sections empty.
"""

_EDITOR_PERSONA = """\
You are Priya Sharma, Managing Editor at InfoRo Media.
Background: 15 years in digital publishing — former content director at Screen Daily,
ex-editor at Variety Digital. Expert at balancing SEO performance with genuine
industry-grade editorial quality in entertainment journalism.
You review articles in their raw HTML form — you can read HTML tags and verify that
styled boxes, tables, and highlights are correctly populated.
You serve an audience of content acquisition executives, streaming strategists,
distributors, and entertainment financiers — not casual fans. You will reject any
article that reads like a fan site, contains unattributed figures, or fails to
answer "what does this mean for the industry?"
"""

_AGENT_PERSONAS = {
    "researcher":  _RESEARCHER_PERSONA,
    "ranker":      _RANKER_PERSONA,
    "factchecker": _FACTCHECKER_PERSONA,
    "writer":      _WRITER_PERSONA,
    "editor":      _EDITOR_PERSONA,
}

# ── Source reputation registry (entertainment) ────────────────────────────────

_SOURCE_REPUTATION = {
    "deadline":                     10,
    "variety":                      10,
    "hollywood reporter":           10,
    "screen daily":                 10,
    "screen international":         9,
    "soompi":                       9,
    "indiewire":                    9,
    "allkpop":                      8,
    "koreaboo":                     8,
    "bollywood hungama":            8,
    "filmfare":                     8,
    "film companion":               8,
    "anime news network":           8,
    "crunchyroll":                  8,
    "japan times":                  8,
    "south china morning post":     8,
    "scmp":                         8,
    "cineuropa":                    8,
    "gold derby":                   7,
    "awards circuit":               7,
    "box office mojo":              7,
    "ndtv":                         7,
    "techcrunch":                   6,
    "the verge":                    6,
    "collider":                     6,
    "screenrant":                   5,
    "cinemablend":                  5,
    "pinkvilla":                    5,
    "unknown":                      3,
}

# ── Article types ─────────────────────────────────────────────────────────────

_ARTICLE_TYPES = {
    "breaking_news",
    "box_office",
    "streaming_data",
    "deal_funding",
    "awards_buzz",
    "talent_movement",
    "platform_strategy",
    "explainer",
}

# ── Trend alignment ───────────────────────────────────────────────────────────

_TREND_ALIGNMENT = [
    "OTT Platform Wars",
    "K-Wave Global Expansion",
    "Franchise IP Arms Race",
    "Indian Cinema Globalization",
    "Awards Circuit Dealmaking",
    "Anime IP Monetization",
    "Arthouse Crossover",
    "Box Office Recovery",
    "Streaming Profitability Pressure",
    "Global Content Localization",
]

# ── SiteConfig ────────────────────────────────────────────────────────────────

SITE = SiteConfig(
    # Identity
    name="inforomedia",
    display_name="InfoRo Media",
    site_url="https://info-ro-media.com",

    # WordPress (admin credentials — articles published under per-category author_id)
    wp_url=os.environ.get("INFOROMEDIA_WP_URL", "https://info-ro-media.com"),
    wp_username=os.environ.get("INFOROMEDIA_WP_USERNAME", ""),
    wp_password=os.environ.get("INFOROMEDIA_WP_PASSWORD", ""),
    wp_api_key=os.environ.get("INFOROMEDIA_WP_API_KEY", ""),

    # Content sources
    categories=CATEGORIES,
    category_feeds=CATEGORY_FEEDS,
    fallback_feeds=FALLBACK_FEEDS,

    # Database (separate MongoDB instance — configure INFOROMEDIA_MONGODB_URI later)
    db_name="inforomedia",

    # LinkedIn
    linkedin_access_token=os.environ.get("INFOROMEDIA_LINKEDIN_ACCESS_TOKEN", ""),
    linkedin_org_urn=os.environ.get("INFOROMEDIA_LINKEDIN_ORG_URN", ""),
    linkedin_person_urn=os.environ.get("INFOROMEDIA_LINKEDIN_PERSON_URN", ""),

    # Twitter/X
    twitter_api_key=os.environ.get("INFOROMEDIA_TWITTER_API_KEY", ""),
    twitter_api_secret=os.environ.get("INFOROMEDIA_TWITTER_API_SECRET", ""),
    twitter_access_token=os.environ.get("INFOROMEDIA_TWITTER_ACCESS_TOKEN", ""),
    twitter_access_secret=os.environ.get("INFOROMEDIA_TWITTER_ACCESS_SECRET", ""),

    # Facebook
    fb_page_id=os.environ.get("INFOROMEDIA_FB_PAGE_ID", ""),
    fb_page_access_token=os.environ.get("INFOROMEDIA_FB_PAGE_ACCESS_TOKEN", ""),

    # Agent overrides
    agent_personas=_AGENT_PERSONAS,
    source_reputation=_SOURCE_REPUTATION,
    article_types=_ARTICLE_TYPES,
    trend_alignment=_TREND_ALIGNMENT,
)
