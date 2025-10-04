from dataclasses import dataclass

from sqlalchemy import delete, insert, select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from app.domain.entities.sentences import ParsedSentenceModel
from app.domain.services.interfaces.sentences import SentencesInterface
from app.infra.db.models.sentences import SentenceDBModel, TokenDBModel


@dataclass
class SentencesAdapter(SentencesInterface):
    _db_engine: Engine
    _sent_model: type[SentenceDBModel] = SentenceDBModel
    _token_model: type[TokenDBModel] = TokenDBModel

    def put_sentence(
        self, transcript_id: int, parsed_sentence: ParsedSentenceModel
    ) -> int:
        with Session(self._db_engine) as session, session.begin():
            sent_insert_query = (
                insert(self._sent_model)
                .values(
                    **(
                        parsed_sentence.model_dump(
                            exclude_none=True, exclude={"tokens"}
                        )
                    )
                    | {"transcript_id": transcript_id}
                )
                .returning(self._sent_model.id)
            )
            sent_id = session.execute(sent_insert_query).scalar_one()

            session.execute(
                insert(self._token_model),
                [
                    {"sent_id": sent_id} | token.model_dump(exclude_none=True)
                    for token in parsed_sentence.tokens
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
