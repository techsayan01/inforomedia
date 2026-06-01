"""
InfoRo Media — RSS feed catalogue and category definitions.

8 categories covering the global entertainment industry, written for an
industry-professional audience (acquisitions execs, platform strategists,
distributors, financiers, and talent agencies).
"""

# ── Hollywood ─────────────────────────────────────────────────────────────────
_DEADLINE        = "https://deadline.com/feed/"
_VARIETY         = "https://variety.com/feed/"
_THR             = "https://www.hollywoodreporter.com/feed/"
_INDIEWIRE       = "https://www.indiewire.com/feed/"
_CINEMA_BLEND    = "https://www.cinemablend.com/rss/news"
_COLLIDER        = "https://collider.com/feed/"
_BOX_OFFICE_MOJO = "https://www.boxofficemojo.com/rss/"
_SCREENRANT      = "https://screenrant.com/feed/"

# ── Bollywood / Indian cinema ─────────────────────────────────────────────────
_BOLLYWOOD_HUNGAMA  = "https://www.bollywoodhungama.com/rss/news.xml"
_FILMFARE           = "https://www.filmfare.com/rss/rss.xml"
_NDTV_MOVIES        = "https://feeds.feedburner.com/ndtvmovies"
_PINKVILLA          = "https://www.pinkvilla.com/rss.xml"
_FILM_COMPANION     = "https://www.filmcompanion.in/feed/"

# ── Korean Wave ───────────────────────────────────────────────────────────────
_SOOMPI       = "https://www.soompi.com/feed"
_ALLKPOP      = "https://www.allkpop.com/rss/news"
_KOREABOO     = "https://www.koreaboo.com/feed/"
_KOREA_HERALD = "https://kpopherald.koreaherald.com/feed/"
_KDRAMA_STARS = "https://www.kdramastars.com/rss/articles.rss"

# ── Japanese cinema & anime ───────────────────────────────────────────────────
_CRUNCHYROLL_NEWS  = "https://www.crunchyroll.com/feed"
_ANIME_NEWS_NET    = "https://www.animenewsnetwork.com/all/rss.xml"
_JAPAN_TIMES_CULT  = "https://www.japantimes.co.jp/culture/feed/"
_SCREEN_ANARCHY    = "https://screenanarchy.com/feed/"

# ── Chinese & East Asian cinema ───────────────────────────────────────────────
_SCMP_ARTS         = "https://www.scmp.com/rss/91/feed"      # SCMP Arts & Culture
_CGTN_ENT          = "https://www.cgtn.com/subscribe/rss/section/culture-s.xml"
_GLOBAL_TIMES_ENT  = "https://www.globaltimes.cn/rss/outbrain.xml"
_FILM_STAGE        = "https://thefilmstage.com/feed/"

# ── World cinema / arthouse ───────────────────────────────────────────────────
_SCREEN_DAILY      = "https://www.screendaily.com/rss"
_CINEUROPA         = "https://cineuropa.org/rss/"
_SIGHT_AND_SOUND   = "https://www.bfi.org.uk/sight-and-sound/rss"
_RFI_CINEMA        = "https://en.rfi.fr/culture/rss"

# ── Streaming & platform ──────────────────────────────────────────────────────
_STREAMING_WARS    = "https://www.streamingmediablog.com/feed"
_THE_VERGE_STREAM  = "https://www.theverge.com/rss/index.xml"
_TECHCRUNCH_MEDIA  = "https://techcrunch.com/category/media-entertainment/feed/"
_ANTENNA_BLOG      = "https://www.antenna.live/rss"

# ── Awards & festivals ────────────────────────────────────────────────────────
_GOLD_DERBY        = "https://www.goldderby.com/feed/"
_AWARDS_CIRCUIT    = "https://www.awardscircuit.com/feed/"
_FESTIVAL_INSIGHT  = "https://www.festivalinsights.com/feed/"


# ── Category definitions ──────────────────────────────────────────────────────

CATEGORIES: list[dict] = [
    {
        "name":             "Hollywood",
        "slug":             "hollywood",
        "author_id":        2,       # Asha Nair — update with real WP user ID
        "image_style":      "cinematic film production Hollywood studio",
        "target_audience":  "studio executives, distributors, content acquisition teams, entertainment financiers",
        "site_display_name": "InfoRo Media",
        "keywords": [
            "hollywood", "box office", "studio", "streaming", "netflix", "disney",
            "warner", "universal", "sony pictures", "paramount", "apple tv",
            "amazon prime", "hbo", "theatrical", "franchise", "sequel",
            "greenlight", "production deal", "acquisition", "prestige",
        ],
    },
    {
        "name":             "Bollywood",
        "slug":             "bollywood",
        "author_id":        3,       # Rohan Mehta — update with real WP user ID
        "image_style":      "bollywood indian cinema film production",
        "target_audience":  "Indian film distributors, OTT platform executives, regional cinema investors",
        "site_display_name": "InfoRo Media",
        "keywords": [
            "bollywood", "indian cinema", "hindi film", "ott", "netflix india",
            "amazon prime india", "disney+ hotstar", "zee5", "sony liv",
            "box office india", "trade", "collection", "first week",
            "south indian", "telugu", "tamil", "pan-india",
            "yash raj", "dharma", "t-series", "eros",
        ],
    },
    {
        "name":             "K-Drama & K-Pop",
        "slug":             "kdrama-kpop",
        "author_id":        4,       # Ji-Yeon Park — update with real WP user ID
        "image_style":      "korean entertainment kpop kdrama seoul",
        "target_audience":  "K-content licensing executives, streaming platform programmers, talent agency professionals",
        "site_display_name": "InfoRo Media",
        "keywords": [
            "kdrama", "k-drama", "kpop", "k-pop", "korean", "hallyu",
            "netflix korea", "tvn", "jtbc", "hybe", "sm entertainment",
            "yg entertainment", "jyp entertainment", "bts", "blackpink",
            "webtoon", "licensing", "global rights", "comeback",
            "streaming rights", "territorial rights",
        ],
    },
    {
        "name":             "Japanese Anime & Cinema",
        "slug":             "japanese-anime",
        "author_id":        5,       # Kenji Watanabe — update with real WP user ID
        "image_style":      "japanese anime cinema tokyo studio",
        "target_audience":  "Anime IP licensing executives, co-production partners, streaming platform acquisitions teams",
        "site_display_name": "InfoRo Media",
        "keywords": [
            "anime", "japanese cinema", "j-film", "studio ghibli", "toei",
            "toho", "shueisha", "manga", "ip licensing", "live-action adaptation",
            "crunchyroll", "funimation", "aniplex", "bandai namco",
            "theatrical anime", "global rights", "co-production", "simulcast",
        ],
    },
    {
        "name":             "Chinese Cinema",
        "slug":             "chinese-cinema",
        "author_id":        6,       # Lin Wei — update with real WP user ID
        "image_style":      "chinese cinema hong kong film industry",
        "target_audience":  "Co-production executives, Asia-Pacific distributors, China market entry strategists",
        "site_display_name": "InfoRo Media",
        "keywords": [
            "chinese cinema", "china box office", "c-drama", "cdrama",
            "hong kong film", "mandarin", "iqiyi", "youku", "tencent video",
            "bilibili", "co-production", "state film bureau", "cfpc",
            "cnki", "quota", "censorship", "golden rooster",
            "hong kong golden horse", "asia-pacific",
        ],
    },
    {
        "name":             "World Cinema",
        "slug":             "world-cinema",
        "author_id":        7,       # Sofia Marchetti — update with real WP user ID
        "image_style":      "international arthouse cinema film festival europe",
        "target_audience":  "Festival acquisitions teams, arthouse distributors, international co-production executives",
        "site_display_name": "InfoRo Media",
        "keywords": [
            "world cinema", "cannes", "venice", "berlin", "toronto tiff",
            "sundance", "arthouse", "european cinema", "french film",
            "latin american cinema", "african cinema", "mena cinema",
            "foreign language", "international distribution",
            "festival premiere", "acquisition", "sales agent", "presales",
        ],
    },
    {
        "name":             "Streaming Wars",
        "slug":             "streaming-wars",
        "author_id":        8,       # Cassandra Rhodes — update with real WP user ID
        "image_style":      "streaming platform digital entertainment technology",
        "target_audience":  "Platform strategy executives, content licensing teams, media analysts, OTT investors",
        "site_display_name": "InfoRo Media",
        "keywords": [
            "netflix", "disney+", "amazon prime video", "apple tv+", "hbo max",
            "max", "paramount+", "peacock", "streaming", "subscriber",
            "churn", "arpu", "content spend", "licensing", "theatrical window",
            "bundling", "ad-supported", "svod", "avod", "fast channels",
            "viewership", "cancellation", "renewal", "slate",
        ],
    },
    {
        "name":             "Awards & Festivals",
        "slug":             "awards-festivals",
        "author_id":        9,       # Daniel Osei — update with real WP user ID
        "image_style":      "film awards ceremony festival red carpet industry",
        "target_audience":  "Acquisitions executives, awards campaign strategists, distribution professionals",
        "site_display_name": "InfoRo Media",
        "keywords": [
            "oscars", "academy awards", "bafta", "cannes", "golden globes",
            "sundance", "tiff", "venice", "berlin berlinale", "biff busan",
            "film festival", "nomination", "awards race", "prestige",
            "awards campaign", "for your consideration", "fyc",
            "palme d'or", "grand prix", "golden lion", "golden bear",
        ],
    },
]

# ── Feed mapping by category slug ─────────────────────────────────────────────

CATEGORY_FEEDS: dict[str, list[str]] = {
    "hollywood": [
        _DEADLINE,
        _VARIETY,
        _THR,
        _INDIEWIRE,
        _BOX_OFFICE_MOJO,
    ],
    "bollywood": [
        _BOLLYWOOD_HUNGAMA,
        _FILMFARE,
        _NDTV_MOVIES,
        _FILM_COMPANION,
        _PINKVILLA,
    ],
    "kdrama-kpop": [
        _SOOMPI,
        _ALLKPOP,
        _KOREABOO,
        _KOREA_HERALD,
    ],
    "japanese-anime": [
        _CRUNCHYROLL_NEWS,
        _ANIME_NEWS_NET,
        _JAPAN_TIMES_CULT,
        _SCREEN_ANARCHY,
    ],
    "chinese-cinema": [
        _SCMP_ARTS,
        _CGTN_ENT,
        _FILM_STAGE,
        _SCREEN_ANARCHY,
    ],
    "world-cinema": [
        _SCREEN_DAILY,
        _CINEUROPA,
        _INDIEWIRE,
        _SIGHT_AND_SOUND,
        _RFI_CINEMA,
    ],
    "streaming-wars": [
        _STREAMING_WARS,
        _VARIETY,
        _DEADLINE,
        _TECHCRUNCH_MEDIA,
        _THE_VERGE_STREAM,
    ],
    "awards-festivals": [
        _GOLD_DERBY,
        _AWARDS_CIRCUIT,
        _SCREEN_DAILY,
        _VARIETY,
        _DEADLINE,
    ],
}

# Fallback feeds — used when primary feeds return fewer than 3 stories.
# Broad entertainment trades that cover all categories.
FALLBACK_FEEDS: list[str] = [
    _VARIETY,
    _DEADLINE,
    _THR,
    _INDIEWIRE,
    _SCREEN_DAILY,
]
