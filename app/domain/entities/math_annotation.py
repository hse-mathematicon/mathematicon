from pydantic import BaseModel


class AnnotationSpanPutModel(BaseModel):
    sent_idx: int
    char_start: int
    char_end: int


class MathEntityPutModel(BaseModel):
    math_tag_id: str
    span: AnnotationSpanPutModel
