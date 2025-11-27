from typing import Optional

from pydantic import BaseModel


class AnnotationSpanPutModel(BaseModel):
    sent_idx: int
    char_start: int
    char_end: int


class MathEntityPutModel(BaseModel):
    math_tag_id: str
    span: AnnotationSpanPutModel


class MathEntityModel(BaseModel):
    math_tag_id: str
    sent_id: int
    tokens_position: list[int]


class MathEntityGetFilterModel(BaseModel):
    math_tag_id_in: Optional[list[str]] = None
