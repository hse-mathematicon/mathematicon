from collections.abc import Iterable

import spacy

from app.domain.entities.sentences import SentencePutModel, TokenPutModel
from app.domain.services.interfaces.language_parser import LanguageParserInterface


class SpacyLanguageParser(LanguageParserInterface):
    def __init__(self, spacy_model: str):
        self._nlp = spacy.load(spacy_model)
        if "conllu_formatter" not in [pipe[0] for pipe in self._nlp.pipeline]:
            self._nlp.add_pipe(
                "conll_formatter", last=True, config={"include_headers": True}
            )

    def parse(self, text: str) -> Iterable[SentencePutModel]:
        doc = self._nlp(text)
        res = []
        for i, sent in enumerate(doc.sents):
            parsed_sent = SentencePutModel(
                tokens=[], position=i, text=sent.text, lemmatized_text=""
            )
            char_offset = 0
            for i, token in enumerate(sent):
                parsed_sent.tokens.append(
                    TokenPutModel(
                        position=i,
                        text=token.text,
                        lemma=token.lemma_,
                        pos=token.pos_,
                        whitespace=bool(token.whitespace_),
                        conll_str=token._.conll_str,
                        char_start=char_offset,
                        char_end=char_offset + len(token.text),
                    )
                )
                char_offset += len(token.text) + len(token.whitespace_)
                parsed_sent.lemmatized_text += f" {token.lemma_}"
            res.append(parsed_sent)
        return res

    def generate_conllu(self, text: str) -> str:
        doc = self._nlp(text)
        return doc._.conll_str
