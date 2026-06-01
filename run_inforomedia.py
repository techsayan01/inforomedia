"""
InfoRo Media — daily pipeline entry point.

Usage:
    python run_inforomedia.py

Environment variables required (set in .env):
    INFOROMEDIA_WP_URL
    INFOROMEDIA_WP_USERNAME
    INFOROMEDIA_WP_PASSWORD
    GEMINI_API_KEY  (or GOOGLE_APPLICATION_CREDENTIALS for service account)
    MONGODB_URI     (shared Atlas cluster) — or INFOROMEDIA_MONGODB_URI once separate cluster is ready
    UNSPLASH_API_KEY
"""

import os
import sys
from pathlib import Path

# Load .env from project root
try:
    from dotenv import load_dotenv
    _env = Path(__file__).parent / ".env"
    if _env.exists():
        load_dotenv(dotenv_path=_env, override=True)
except ImportError:
    pass

from core import db, llm
from pipelines.daily_news import run
from sites.inforomedia.config import SITE


def main() -> None:
    # Allow overriding MongoDB URI per site when separate cluster is ready
    mongo_uri_override = os.environ.get("INFOROMEDIA_MONGODB_URI", "")
    if mongo_uri_override:
        os.environ["MONGODB_URI"] = mongo_uri_override

    SITE.validate()
    db.configure(SITE.db_name)
    llm.init_client(db_log_fn=db.log_llm_usage)
    run(SITE)


if __name__ == "__main__":
    main()
