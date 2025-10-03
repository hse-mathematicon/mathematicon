from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from app.infra.db.models.base import BaseModel


class TranscriptDBModel(BaseModel):
    __tablename__ = "transcripts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    filename: Mapped[str] = mapped_column(unique=True)
    src_url: Mapped[str] = mapped_column(unique=True)
    text: Mapped[str] = mapped_column(Text, deferred=True)
    title: Mapped[str] = mapped_column()
    timecode_start: Mapped[str] = mapped_column()
    timecode_end: Mapped[str] = mapped_column()
    math_branch: Mapped[str] = mapped_column()
    difficulty: Mapped[str] = mapped_column()
