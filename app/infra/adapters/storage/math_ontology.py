from collections import defaultdict
from dataclasses import dataclass

from sqlalchemy import delete, insert, select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from app.domain.entities.math_ontology import (
    MathTagAttributeModel,
    MathTagGetFilterModel,
    MathTagModel,
)
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
                    | {"math_tag_id": math_tag.inception_id}
                    for math_tag in math_tags
                    for attr in math_tag.attrs
                ],
            )

    def delete_math_ontology(self) -> None:
        with Session(self._db_engine) as session, session.begin():
            session.execute(delete(self._tag_attr_model))
            session.execute(delete(self._tag_model))

    def get_tag_descendants(self, math_tag_id: str) -> list[str]:
        with Session(self._db_engine) as session:
            tags = session.execute(select(self._tag_model)).scalars()

            children_map = defaultdict(list)
            for tag in tags:
                children_map[tag.parent_id].append(tag.inception_id)

            result = []
            stack = children_map.get(math_tag_id, [])

            while stack:
                child = stack.pop()
                result.append(child)
                stack.extend(children_map.get(child, []))

            return result

    def get_math_tags(self, filters: MathTagGetFilterModel) -> list[MathTagModel]:
        query = select(self._tag_model)
        if filters.math_tag_id:
            query = query.where(self._tag_model.inception_id == filters.math_tag_id)

        if filters.attr_key or filters.attr_value or filters.attr_lang:
            query = query.join(
                self._tag_attr_model,
                self._tag_model.inception_id == self._tag_attr_model.math_tag_id,
            )

        if filters.attr_key:
            query = query.filter(self._tag_attr_model.key == filters.attr_key)

        if filters.attr_value:
            query = query.filter(self._tag_attr_model.value == filters.attr_value)

        if filters.attr_lang:
            query = query.filter(self._tag_attr_model.language == filters.attr_lang)

        with Session(self._db_engine) as session:
            result = session.execute(query).scalars()
            return [
                MathTagModel(
                    inception_id=tag.inception_id,
                    parent_id=tag.parent_id,
                    attrs=[
                        MathTagAttributeModel.model_validate(attr) for attr in tag.atts
                    ],
                )
                for tag in result
            ]
