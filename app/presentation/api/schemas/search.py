from pydantic import BaseModel

from app.domain.entities.search import MathTagSentenceMatchInfo


class MathTagSearchResult(BaseModel):
    query: str
    result: list[MathTagSentenceMatchInfo]
    total: int
