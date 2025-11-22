from dataclasses import dataclass

from sqlalchemy import delete, select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from app.domain.entities.math_annotation import MathEntityPutModel
from app.domain.services.interfaces.math_annotation import MathAnnotationInterface
from app.infra.db.models.math_annotation import MathEntityDBModel
from app.infra.db.models.sentences import SentenceDBModel


@dataclass
class MathAnnotationAdapter(MathAnnotationInterface):
    _db_engine: Engine
    _math_entity_model: type[MathEntityDBModel] = MathEntityDBModel
    _sent_model: type[SentenceDBModel] = SentenceDBModel

    def put_math_entities(
        self, transcript_id: int, math_entities: list[MathEntityPutModel]
    ) -> None:
        """Добавить математическую разметку для текста."""
        with Session(self._db_engine) as session, session.begin():
            sentences_query = session.execute(
                select(self._sent_model.id, self._sent_model.position).where(
                    self._sent_model.transcript_id == transcript_id
                )
            ).fetchall()
            sentences_position = {
                position: sent_id for sent_id, position in sentences_query
            }

            for entity in math_entities:
                session.add(
                    self._math_entity_model(
                        math_tag_id=entity.math_tag_id,
                        sent_id=sentences_position[entity.span.sent_idx],
                        char_start=entity.span.char_start,
                        char_end=entity.span.char_end,
                    )
                )

    def delete_math_entities(self, transcript_id: int) -> None:
        with Session(self._db_engine) as session, session.begin():
            sent_ids = session.execute(
                select(self._sent_model.id).where(
                    self._sent_model.transcript_id == transcript_id
                )
            ).scalars()
            query = delete(self._math_entity_model).where(
                self._math_entity_model.sent_id.in_(sent_ids)
            )

            session.execute(query)
