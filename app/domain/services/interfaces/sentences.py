from abc import abstractmethod
from typing import Optional, Protocol

from app.domain.entities.sentences import (
    GrammarAnnotationStatsModel,
    SentenceFilterModel,
    SentenceInfoModel,
    SentencePutModel,
    TokenInfoModel,
)


class SentencesInterface(Protocol):
    @abstractmethod
    def put_sentence(self, transcript_id: int, sentence: SentencePutModel) -> int: ...

    @abstractmethod
    def get_sentence(self, sent_id: int) -> Optional[SentenceInfoModel]: ...

    @abstractmethod
    def get_sentences(
        self, filters: SentenceFilterModel
    ) -> list[SentenceInfoModel]: ...

    @abstractmethod
    def get_sentence_tokens(self, sent_id: int) -> list[TokenInfoModel]: ...

    @abstractmethod
    def get_grammar_annotation_stats(
        self, transcript_id: int
    ) -> Optional[GrammarAnnotationStatsModel]: ...
