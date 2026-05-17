import re
import unicodedata

_ZERO_WIDTH = re.compile(r"[​-‍﻿­]")
_MULTIPLE_WS = re.compile(r"[ \t]+")

# Cyrillic lookalike → Latin; number-for-letter substitutions spammers use
_HOMOGLYPH_MAP: dict[str, str] = {
    "а": "a",  # а → a
    "е": "e",  # е → e
    "о": "o",  # о → o
    "р": "p",  # р → p
    "с": "c",  # с → c
    "х": "x",  # х → x
    "і": "i",  # і → i
    "0": "o",
    "1": "l",
    "3": "e",
    "4": "a",
    "5": "s",
    "@": "a",
}


class TextNormalizer:
    def normalize(self, text: str) -> str:
        """Production-safe normalization — preserves script for language detection."""
        text = unicodedata.normalize("NFC", text)
        text = _ZERO_WIDTH.sub("", text)
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        text = _MULTIPLE_WS.sub(" ", text)
        return text.strip()

    def normalize_for_matching(self, text: str) -> str:
        """
        Deobfuscated lowercase form used by rule engine and keyword matcher.
        Maps homoglyphs to their canonical ASCII equivalents so spammers cannot
        evade rules by replacing 'о' with 'o' or '0'.
        """
        text = self.normalize(text).lower()
        for char, replacement in _HOMOGLYPH_MAP.items():
            text = text.replace(char, replacement)
        return text
