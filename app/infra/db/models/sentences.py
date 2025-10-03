from typing import Optional

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.infra.db.models.base import BaseModel


class SentenceDBModel(BaseModel):
    __tablename__ = "sentences"
    __table_args__ = (UniqueConstraint("transcript_id", "position"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    transcript_id: Mapped[int] = mapped_column(ForeignKey("transcripts.id"))
    position: Mapped[int] = mapped_column()
    text: Mapped[str] = mapped_column()
    lemmatized_text: Mapped[str] = mapped_column()
    timecode_start: Mapped[Optional[str]] = mapped_column()


class TokenDBModel(BaseModel):
    __tablename__ = "tokens"

    sent_id: Mapped[int] = mapped_column(ForeignKey("sentences.id"), primary_key=True)
    position: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column()
    whitespace: Mapped[bool] = mapped_column()
    lemma: Mapped[str] = mapped_column()
    pos: Mapped[str] = mapped_column()
    conll_str: Mapped[str] = mapped_column()
    char_start: Mapped[int] = mapped_column()
    char_end: Mapped[int] = mapped_column()
