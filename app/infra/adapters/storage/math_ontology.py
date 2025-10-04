from dataclasses import dataclass

from sqlalchemy import delete, insert
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from app.domain.entities.math_ontology import MathTagModel
from app.domain.services.interfaces.math_ontology import MathOntologyInterface
from app.infra.db.models.math_ontology import MathTagAttributeDBModel, MathTagDBModel


@dataclass
class MathOntologyAdapter(MathOntologyInterface):
    _db_engine: Engine
    _tag_model: type[MathTagDBModel] = MathTagDBModel
    _tag_attr_model: type[MathTagAttributeDBModel] = MathTagAttributeDBModel

    def put_math_ontology(self, math_tags: list[MathTagModel]) -> None:
        with Session(self._db_engine) as session, session.begin():
            session.execute(
                insert(self._tag_model),
                [
                    tag.model_dump(exclude={"attrs"}, exclude_none=True)
                    for tag in math_tags
                ],
            )

            session.execute(
                insert(self._tag_attr_model),
                [
                    attr.model_dump(exclude_none=True)
                    for math_tag in math_tags
                    for attr in math_tag.attrs
                ],
            )

    def delete_math_ontology(self) -> None:
        with Session(self._db_engine) as session, session.begin():
            session.execute(delete(self._tag_attr_model))
            session.execute(delete(self._tag_model))
