from __future__ import annotations

import importlib
import types


def get_strings(lang: str) -> types.ModuleType:
    """Load locale string module for the given language code."""
    _MAP = {
        "uz_lat": "locales.uz_lat",
        "uz_lat_cyr": "locales.uz_cyr",
        "uz_cyr": "locales.uz_cyr",
        "ru": "locales.ru",
        "en": "locales.en",
    }
    module_path = _MAP.get(lang, "locales.uz_lat")
    return importlib.import_module(module_path)
