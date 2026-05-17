from core.preprocessor.base import BasePreprocessor, ProcessedMessage
from core.preprocessor.cleaner import TextCleaner
from core.preprocessor.language import detect_language
from core.preprocessor.normalizer import TextNormalizer


class PreprocessingPipeline(BasePreprocessor):
    def __init__(self) -> None:
        self._normalizer = TextNormalizer()
        self._cleaner = TextCleaner()

    async def process(self, text: str) -> ProcessedMessage:
        normalized = self._normalizer.normalize(text)
        cleaned = self._cleaner.clean(normalized)
        language = await detect_language(normalized)

        words = normalized.split()
        word_count = len(words)
        is_mostly_emoji = cleaned.emoji_count > max(word_count, 1) * 0.5

        return ProcessedMessage(
            original=text,
            normalized=normalized,
            language=language,
            word_count=word_count,
            char_count=len(normalized),
            has_urls=bool(cleaned.urls),
            has_mentions=bool(cleaned.mentions),
            is_mostly_emoji=is_mostly_emoji,
            extracted_urls=cleaned.urls,
            extracted_mentions=cleaned.mentions,
            extracted_phones=cleaned.phone_numbers,
            emoji_count=cleaned.emoji_count,
        )
