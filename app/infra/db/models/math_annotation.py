from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.infra.db.models.base import BaseModel


class MathEntityDBModel(BaseModel):
    __tablename__ = "math_entities"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    math_tag_id: Mapped[str] = mapped_column()

    sent_id: Mapped[int] = mapped_column(ForeignKey("sentences.id"))
    char_start: Mapped[str] = mapped_column()
    char_end: Mapped[str] = mapped_column()
