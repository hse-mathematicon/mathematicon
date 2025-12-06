from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infra.db.models.base import BaseModel


class MathTagDBModel(BaseModel):
    __tablename__ = "math_tags"

    inception_id: Mapped[str] = mapped_column(primary_key=True)
    parent_id: Mapped[Optional[str]] = mapped_column()

    atts: Mapped[list["MathTagAttributeDBModel"]] = relationship(lazy="select")


class MathTagAttributeDBModel(BaseModel):
    __tablename__ = "math_tag_attributes"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    math_tag_id: Mapped[str] = mapped_column(ForeignKey("math_tags.inception_id"))
    key: Mapped[str] = mapped_column()
    value: Mapped[str] = mapped_column()
    language: Mapped[str] = mapped_column()
