from pydantic import BaseModel


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
