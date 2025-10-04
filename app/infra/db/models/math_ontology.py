from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.infra.db.models.base import BaseModel


class MathTagDBModel(BaseModel):
    __tablename__ = "math_tags"

    inception_id: Mapped[str] = mapped_column(primary_key=True)
    parent_id: Mapped[Optional[str]] = mapped_column()


class MathTagAttributeDBModel(BaseModel):
    __tablename__ = "math_tag_attributes"

    math_tag_id: Mapped[str] = mapped_column(
        ForeignKey("math_tags.inception_id"), primary_key=True
    )
    key: Mapped[str] = mapped_column(primary_key=True)
    value: Mapped[str] = mapped_column()
    language: Mapped[str] = mapped_column(primary_key=True)
