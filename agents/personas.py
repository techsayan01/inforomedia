"""
Agent persona configuration — set once per run via configure().

Agents import get_persona(), get_source_reputation(), get_article_types(),
and get_trend_alignment() instead of hardcoding site-specific strings.

GrowStream Media passes nothing → agents fall back to their built-in defaults.
InfoRo Media (and any future site) passes overrides at startup.
"""

from __future__ import annotations

_personas: dict[str, str] = {}
_source_reputation: dict[str, int] = {}
_article_types: set[str] = set()
_trend_alignment: list[str] = []


def configure(
    personas: dict[str, str] | None = None,
    source_reputation: dict[str, int] | None = None,
    article_types: set[str] | None = None,
    trend_alignment: list[str] | None = None,
) -> None:
    """Set site-specific overrides. Call once at pipeline startup."""
    global _personas, _source_reputation, _article_types, _trend_alignment
    _personas           = dict(personas or {})
    _source_reputation  = dict(source_reputation or {})
    _article_types      = set(article_types or set())
    _trend_alignment    = list(trend_alignment or [])


def get_persona(agent: str, default: str = "") -> str:
    return _personas.get(agent, default)


def get_source_reputation() -> dict[str, int]:
    return _source_reputation


def get_article_types() -> set[str]:
    return _article_types


def get_trend_alignment() -> list[str]:
    return _trend_alignment
