from abc import abstractmethod
from typing import Protocol

from app.domain.entities.math_annotation import MathEntityPutModel


class MathAnnotationInterface(Protocol):
    @abstractmethod
    def put_math_entities(
        self, transcript_id: int, math_entities: list[MathEntityPutModel]
    ) -> None:
        """Добавить математическую разметку для текста."""
