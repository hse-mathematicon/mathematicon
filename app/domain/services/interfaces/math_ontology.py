from abc import abstractmethod
from typing import Protocol

from app.domain.entities.math_ontology import MathTagModel


class MathOntologyInterface(Protocol):
    @abstractmethod
    def put_math_ontology(self, math_tags: list[MathTagModel]) -> None: ...
