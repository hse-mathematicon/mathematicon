from typing import Optional

from pydantic import BaseModel

from app.domain.entities.math_annotation import MathEntityModel
from app.domain.entities.sentences import TokenInfoModel


class SearchResultTranscriptInfo(BaseModel):
    src_url: str


class SearchResultSentenceInfo(BaseModel):
    sent_id: int
    tokens: list[TokenInfoModel]
    left_context: Optional[str] = None
    right_context: Optional[str] = None
    timecode_start: Optional[str] = None


class MathTagSentenceMatchInfo(BaseModel):
    math_entities: list[MathEntityModel]
    matched_tokens: list[int]
    transcript_info: SearchResultTranscriptInfo
    sent_info: SearchResultSentenceInfo
