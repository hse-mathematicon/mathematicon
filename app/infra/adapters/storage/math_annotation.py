from dataclasses import dataclass

from sqlalchemy import delete, select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from app.domain.entities.math_annotation import (
    MathEntityGetFilterModel,
    MathEntityModel,
    MathEntityPutModel,
)
from app.domain.services.interfaces.math_annotation import MathAnnotationInterface
from app.infra.db.models.math_annotation import MathEntityDBModel
from app.infra.db.models.sentences import SentenceDBModel, TokenDBModel


@dataclass
class MathAnnotationAdapter(MathAnnotationInterface):
    _db_engine: Engine
    _math_entity_model: type[MathEntityDBModel] = MathEntityDBModel
    _sent_model: type[SentenceDBModel] = SentenceDBModel
    _token_model: type[TokenDBModel] = TokenDBModel

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

    def get_math_entities(
        self, filters: MathEntityGetFilterModel
    ) -> list[MathEntityModel]:
        query = select(
            self._math_entity_model.id,
            self._math_entity_model.math_tag_id,
            self._math_entity_model.sent_id,
            self._token_model.position,
        ).join(
            self._token_model,
            (self._token_model.sent_id == self._math_entity_model.sent_id)
            & (self._token_model.char_start >= self._math_entity_model.char_start)
            & (self._token_model.char_end <= self._math_entity_model.char_end),
        )
        if filters.math_tag_id_in:
            query.filter(
                self._math_entity_model.math_tag_id.in_(filters.math_tag_id_in)
            )

        entities = {}
        with Session(self._db_engine) as session:
            result = session.execute(query).all()
            for res in result:
                if res[0] not in entities:
                    entities[res[0]] = MathEntityModel(
                        math_tag_id=res[1], sent_id=res[2], tokens_position=[res[3]]
                    )
                else:
                    entities[res[0]].tokens_position.append(res[3])

        return list(entities.values())

    def check_math_entities_exist(self, filters: MathEntityGetFilterModel) -> bool:
        query = select(self._math_entity_model)

        if filters.transcript_id:
            query = query.join(
                self._sent_model, self._math_entity_model.sent_id == self._sent_model.id
            ).where(self._sent_model.transcript_id == filters.transcript_id)

        with Session(self._db_engine) as session:
            result = session.execute(query).scalars().all()
            return bool(result)
