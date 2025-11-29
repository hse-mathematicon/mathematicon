from abc import abstractmethod
from typing import Protocol

from app.domain.entities.math_ontology import MathTagGetFilterModel, MathTagModel


class MathOntologyInterface(Protocol):
    @abstractmethod
    def put_math_ontology(self, math_tags: list[MathTagModel]) -> None: ...

    @abstractmethod
    def get_tag_descendants(self, math_tag_id: str) -> list[str]: ...

    @abstractmethod
    def get_math_tags(self, filters: MathTagGetFilterModel) -> list[MathTagModel]: ...
