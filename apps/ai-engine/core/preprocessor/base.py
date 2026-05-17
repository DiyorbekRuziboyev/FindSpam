from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from core.preprocessor.language import Language


@dataclass
class ProcessedMessage:
    original: str
    normalized: str
    language: Language
    word_count: int
    char_count: int
    has_urls: bool
    has_mentions: bool
    is_mostly_emoji: bool
    extracted_urls: list[str] = field(default_factory=list)
    extracted_mentions: list[str] = field(default_factory=list)
    extracted_phones: list[str] = field(default_factory=list)
    emoji_count: int = 0


class BasePreprocessor(ABC):
    @abstractmethod
    async def process(self, text: str) -> ProcessedMessage: ...
