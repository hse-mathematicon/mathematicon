from dataclasses import dataclass
from typing import Optional

from sqlalchemy import delete, distinct, func, insert, select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from app.domain.entities.sentences import (
    GrammarAnnotationStatsModel,
    SentenceFilterModel,
    SentenceInfoModel,
    SentencePutModel,
    TokenInfoModel,
)
from app.domain.services.interfaces.sentences import SentencesInterface
from app.infra.db.models.sentences import SentenceDBModel, TokenDBModel


@dataclass
class SentencesAdapter(SentencesInterface):
    _db_engine: Engine
    _sent_model: type[SentenceDBModel] = SentenceDBModel
    _token_model: type[TokenDBModel] = TokenDBModel

    def put_sentence(self, transcript_id: int, sentence: SentencePutModel) -> int:
        with Session(self._db_engine) as session, session.begin():
            sent_insert_query = (
                insert(self._sent_model)
                .values(
                    **(sentence.model_dump(exclude_none=True, exclude={"tokens"}))
                    | {"transcript_id": transcript_id}
                )
                .returning(self._sent_model.id)
            )
            sent_id = session.execute(sent_insert_query).scalar_one()

            session.execute(
                insert(self._token_model),
                [
                    {"sent_id": sent_id} | token.model_dump(exclude_none=True)
                    for token in sentence.tokens
                ],
            )

            return sent_id

    def delete_sentences(self, transcript_id: int) -> None:
        with Session(self._db_engine) as session, session.begin():
            sentence_ids = session.execute(
                select(self._sent_model.id).where(
                    self._sent_model.transcript_id == transcript_id
                )
            ).scalars()
            if not sentence_ids:
                return
            session.execute(
                delete(self._token_model).where(
                    self._token_model.sent_id.in_(sentence_ids)
                )
            )
            session.execute(
                delete(self._sent_model).where(
                    self._sent_model.transcript_id == transcript_id
                )
            )

    def get_sentence(self, sent_id: int) -> Optional[SentenceInfoModel]:
        sentence = self.get_sentences(SentenceFilterModel(id=sent_id))
        return sentence[0] if sentence else None

    def get_sentences(self, filters: SentenceFilterModel) -> list[SentenceInfoModel]:
        query = select(self._sent_model).filter_by(
            **filters.model_dump(exclude_none=True)
        )
        with Session(self._db_engine) as session:
            sentences = session.execute(query)
            return [
                SentenceInfoModel.model_validate(info) for info in sentences.scalars()
            ]

    def get_sentence_tokens(self, sent_id: int) -> list[TokenInfoModel]:
        query = (
            select(self._token_model)
            .where(self._token_model.sent_id == sent_id)
            .order_by(self._token_model.position)
        )
        with Session(self._db_engine) as session:
            tokens = session.execute(query)
            return [TokenInfoModel.model_validate(info) for info in tokens.scalars()]

    def get_grammar_annotation_stats(
        self, transcript_id: int
    ) -> Optional[GrammarAnnotationStatsModel]:
        query = (
            select(
                func.count(distinct(self._sent_model.id)).label("sentence_count"),
                func.count(self._token_model.position).label("token_count"),
            )
            .select_from(self._sent_model)
            .join(
                self._token_model,
                self._token_model.sent_id == self._sent_model.id,
                isouter=True,
            )
            .where(self._sent_model.transcript_id == transcript_id)
        )

        with Session(self._db_engine) as session:
            result = session.execute(query).one()

            return (
                GrammarAnnotationStatsModel(
                    sentence_count=result.sentence_count,
                    token_count=result.token_count,
                )
                if result.sentence_count
                else None
            )
