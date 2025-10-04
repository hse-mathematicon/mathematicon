from abc import abstractmethod
from collections.abc import Iterable
from typing import Protocol

from app.domain.entities.sentences import ParsedSentenceModel


class LanguageParserInterface(Protocol):
    @abstractmethod
    def parse(self, text: str) -> Iterable[ParsedSentenceModel]: ...

    @abstractmethod
    def generate_conllu(self, text: str) -> str: ...
