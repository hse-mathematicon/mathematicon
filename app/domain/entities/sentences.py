from pydantic import BaseModel


class TokenInSentenceModel(BaseModel):
    position: int
    text: str
    lemma: str
    pos: str
    whitespace: bool
    conll_str: str
    char_start: int
    char_end: int


class ParsedSentenceModel(BaseModel):
    position: int
    text: str
    lemmatized_text: str
    tokens: list[TokenInSentenceModel]
