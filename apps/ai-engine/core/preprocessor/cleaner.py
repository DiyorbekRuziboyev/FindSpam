import re
from dataclasses import dataclass, field

_URL_RE = re.compile(
    r"https?://[^\s<>\"{}|\\^`\[\]]+"
    r"|(?:www\.|t\.me/|@)[^\s<>\"{}|\\^`\[\]]+",
    re.IGNORECASE,
)
_MENTION_RE = re.compile(r"@[\w]{3,}")
_HASHTAG_RE = re.compile(r"#[\w]+")
_PHONE_RE = re.compile(r"(?:\+?[78])[\s\-(]?(?:\d[\s\-()]?){9,15}")
_EMOJI_RE = re.compile(
    r"[\U0001F300-\U0001F9FF\U00002702-\U000027B0\U000024C2-\U0001F251]+",
    re.UNICODE,
)


@dataclass
class CleanedText:
    cleaned: str
    urls: list[str] = field(default_factory=list)
    mentions: list[str] = field(default_factory=list)
    hashtags: list[str] = field(default_factory=list)
    phone_numbers: list[str] = field(default_factory=list)
    emoji_count: int = 0
    has_external_links: bool = False


class TextCleaner:
    def clean(self, text: str, mask_entities: bool = False) -> CleanedText:
        urls = _URL_RE.findall(text)
        mentions = _MENTION_RE.findall(text)
        hashtags = _HASHTAG_RE.findall(text)
        phones = _PHONE_RE.findall(text)
        emojis = _EMOJI_RE.findall(text)

        cleaned = text
        if mask_entities:
            cleaned = _URL_RE.sub("[URL]", cleaned)
            cleaned = _MENTION_RE.sub("[MENTION]", cleaned)
            cleaned = _EMOJI_RE.sub("", cleaned)

        return CleanedText(
            cleaned=cleaned.strip(),
            urls=urls,
            mentions=mentions,
            hashtags=hashtags,
            phone_numbers=phones,
            emoji_count=len(emojis),
            has_external_links=any(
                u.startswith(("http://", "https://")) for u in urls
            ),
        )
