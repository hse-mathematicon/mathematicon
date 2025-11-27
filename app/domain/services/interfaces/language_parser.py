from abc import abstractmethod
from collections.abc import Iterable
from typing import Protocol

from app.domain.entities.sentences import SentencePutModel


class LanguageParserInterface(Protocol):
    @abstractmethod
    def parse(self, text: str) -> Iterable[SentencePutModel]: ...

    @abstractmethod
    def generate_conllu(self, text: str) -> str: ...
