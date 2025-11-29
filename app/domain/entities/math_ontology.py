from typing import Optional

from pydantic import BaseModel, ConfigDict


class MathTagAttributeModel(BaseModel):
    key: str
    language: str
    value: str

    model_config = ConfigDict(from_attributes=True)


class MathTagModel(BaseModel):
    inception_id: str
    parent_id: Optional[str] = None
    attrs: list[MathTagAttributeModel]

    model_config = ConfigDict(from_attributes=True)


class MathTagGetFilterModel(BaseModel):
    math_tag_id: Optional[str] = None
    attr_key: Optional[str] = None
    attr_value: Optional[str] = None
    attr_lang: Optional[str] = None
