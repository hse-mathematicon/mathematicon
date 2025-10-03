from dataclasses import dataclass
from typing import Optional

from sqlalchemy import delete, insert, select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from app.domain.entities.transcripts import (
    TranscriptGetFiltersModel,
    TranscriptInfoModel,
    TranscriptUploadModel,
)
from app.infra.db.models.transcripts import TranscriptDBModel


@dataclass
class TranscriptsAdapter:
    _db_engine: Engine
    _model: type[TranscriptDBModel] = TranscriptDBModel

    def add_transcript(self, put_transcript: TranscriptUploadModel) -> int:
        query = (
            insert(self._model)
            .values(**put_transcript.model_dump(exclude_none=True))
            .returning(self._model.id)
        )
        with Session(self._db_engine) as session, session.begin():
            inserted = session.execute(query)
            return inserted.scalar_one()

    def get_transcript_info(self, transcript_id: int) -> Optional[TranscriptInfoModel]:
        query = select(self._model).where(self._model.id == transcript_id)

        with Session(self._db_engine) as session:
            result = session.execute(query).scalar_one_or_none()
            if result is None:
                return None
            return TranscriptInfoModel.model_validate(result)

    def get_transcripts_info_by_filters(
        self, filters: TranscriptGetFiltersModel
    ) -> list[TranscriptInfoModel]:
        query = select(self._model).filter_by(**filters.model_dump(exclude_none=True))
        with Session(self._db_engine) as session:
            transcripts = session.execute(query)
            return [
                TranscriptInfoModel.model_validate(info)
                for info in transcripts.scalars()
            ]

    def delete_transcript(self, transcript_id: int) -> None:
        query = delete(self._model).where(self._model.id == transcript_id)

        with Session(self._db_engine) as session, session.begin():
            session.execute(query)
