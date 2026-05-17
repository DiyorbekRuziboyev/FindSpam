import re

import numpy as np

from core.features.base import BaseFeatureExtractor, FeatureVector

_SHORTENER_DOMAINS = frozenset(
    {
        "bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly", "is.gd",
        "buff.ly", "rebrand.ly", "cutt.ly", "short.io", "tiny.cc",
    }
)

_SUSPICIOUS_TLDS = re.compile(r"\.(xyz|top|click|win|loan|gq|tk|ml|ga|cf|pw|work|date|download|review|country)\b", re.IGNORECASE)

_BRAND_IMPERSONATION = re.compile(
    r"(paypa1|payp4l|g00gle|g0ogle|telegr4m|te1egram|faceb00k|faceb0ok|inst4gram|amaz0n|appl3)\.",
    re.IGNORECASE,
)

_IP_URL_RE = re.compile(r"https?://\d{1,3}(?:\.\d{1,3}){3}(?::\d+)?(?:/|$)")
_URL_RE = re.compile(r"https?://[^\s<>\"{}|\\^`\[\]]+|(?:www\.)[^\s<>\"{}|\\^`\[\]]+", re.IGNORECASE)

_FEATURE_NAMES = [
    "has_url",
    "url_count",
    "has_shortener",
    "has_suspicious_tld",
    "has_brand_impersonation",
    "has_ip_url",
    "max_url_length_ratio",
    "url_density",
]


class URLFeatureExtractor(BaseFeatureExtractor):
    @property
    def name(self) -> str:
        return "url"

    def extract(self, text: str, **context: object) -> FeatureVector:
        zeros = np.zeros(len(_FEATURE_NAMES), dtype=np.float32)
        if not text:
            return FeatureVector(name=self.name, features=zeros, feature_names=_FEATURE_NAMES)

        urls = _URL_RE.findall(text)
        url_count = len(urls)

        if url_count == 0:
            return FeatureVector(name=self.name, features=zeros, feature_names=_FEATURE_NAMES)

        has_shortener = any(s in url for url in urls for s in _SHORTENER_DOMAINS)
        has_suspicious_tld = any(_SUSPICIOUS_TLDS.search(url) for url in urls)
        has_brand_impersonation = any(_BRAND_IMPERSONATION.search(url) for url in urls)
        has_ip_url = any(_IP_URL_RE.match(url) for url in urls)

        max_url_len = max(len(url) for url in urls)
        text_len = max(len(text), 1)

        features = np.array(
            [
                1.0,
                min(url_count, 10) / 10.0,
                1.0 if has_shortener else 0.0,
                1.0 if has_suspicious_tld else 0.0,
                1.0 if has_brand_impersonation else 0.0,
                1.0 if has_ip_url else 0.0,
                min(max_url_len, 200) / 200.0,
                min(url_count, 5) / max(len(text.split()), 1),
            ],
            dtype=np.float32,
        )

        return FeatureVector(name=self.name, features=features, feature_names=_FEATURE_NAMES)
