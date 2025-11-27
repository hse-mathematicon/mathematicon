from typing import Optional

from pydantic import BaseModel, ConfigDict


class TokenPutModel(BaseModel):
    position: int
    text: str
    lemma: str
    pos: str
    whitespace: bool
    conll_str: str
    char_start: int
    char_end: int


class SentencePutModel(BaseModel):
    position: int
    text: str
    lemmatized_text: str
    tokens: list[TokenPutModel]


class TokenInfoModel(BaseModel):
    position: int
    text: str
    lemma: str
    pos: str
    whitespace: bool


class SentenceInfoModel(BaseModel):
    id: int
    transcript_id: int
    position: int
    text: str
    timecode_start: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class SentenceFilterModel(BaseModel):
    id: Optional[int] = None
    transcript_id: Optional[int] = None
    position: Optional[int] = None
