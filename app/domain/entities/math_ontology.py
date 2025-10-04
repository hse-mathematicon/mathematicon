from typing import Optional

from pydantic import BaseModel


class MathTagAttributeModel(BaseModel):
    math_tag_id: str
    key: str
    language: str
    value: str


class MathTagModel(BaseModel):
    inception_id: str
    parent_id: Optional[str] = None
    attrs: list[MathTagAttributeModel]
