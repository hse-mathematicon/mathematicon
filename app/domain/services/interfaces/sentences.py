from abc import abstractmethod
from typing import Protocol

from app.domain.entities.sentences import ParsedSentenceModel


class SentencesInterface(Protocol):
    @abstractmethod
    def put_sentence(
        self, transcript_id: int, sentence: ParsedSentenceModel
    ) -> int: ...
