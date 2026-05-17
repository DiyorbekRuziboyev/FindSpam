"""
Language detection with Uzbek Latin / Uzbek Cyrillic disambiguation.

langdetect returns 'uz' for BOTH Uzbek Latin and Uzbek Cyrillic — it cannot
distinguish them. We apply a Cyrillic-character-ratio heuristic after langdetect
confirms the language is Uzbek.

langdetect is synchronous and CPU-bound (Markov chain detector). All calls are
wrapped in asyncio.to_thread() to avoid blocking the event loop.
"""
from __future__ import annotations

import asyncio
import re
from enum import StrEnum

_CYRILLIC_RE = re.compile(r"[Ѐ-ӿ]")
_CYRILLIC_THRESHOLD = 0.25  # >25% Cyrillic chars → Uzbek Cyrillic


class Language(StrEnum):
    UZ_LATIN = "uz_latin"
    UZ_CYRILLIC = "uz_cyrillic"
    RU = "ru"
    EN = "en"
    UNKNOWN = "unknown"


def _uzbek_variant(text: str) -> Language:
    total = len(text.strip())
    if total == 0:
        return Language.UNKNOWN
    cyrillic = len(_CYRILLIC_RE.findall(text))
    return Language.UZ_CYRILLIC if cyrillic / total > _CYRILLIC_THRESHOLD else Language.UZ_LATIN


def _sync_detect(text: str) -> str:
    from langdetect import detect, LangDetectException

    try:
        return detect(text)
    except LangDetectException:
        return "unknown"


async def detect_language(text: str) -> Language:
    if not text or not text.strip():
        return Language.UNKNOWN

    lang_code = await asyncio.to_thread(_sync_detect, text)

    if lang_code == "uz":
        return _uzbek_variant(text)

    _MAP: dict[str, Language] = {
        "ru": Language.RU,
        "en": Language.EN,
    }
    return _MAP.get(lang_code, Language.UNKNOWN)
