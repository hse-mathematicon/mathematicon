from bisect import bisect_left
from dataclasses import dataclass
from typing import BinaryIO

from bs4 import BeautifulSoup
from loguru import logger
from pydantic import BaseModel

from app.domain.entities.math_annotation import (
    AnnotationSpanPutModel,
    MathEntityPutModel,
)
from app.domain.services.exceptions import ParseError
from app.domain.services.interfaces.math_annotation import MathAnnotationInterface


class SentenceXMLTag(BaseModel):
    xmi_id: str
    begin: int
    end: int


class MathEntityXMLTag(BaseModel):
    xmi_id: str
    begin: int
    end: int
    math_tag: str


@dataclass
class MathAnnotationService:
    _math_annotation_adapter: MathAnnotationInterface
    _inception_tag_prefix: str

    def load_math_annotation(
        self, transcript_id: int, annotation_file: BinaryIO
    ) -> list[str]:
        """Загрузить математическую разметку из файла."""
        error_messages: list[str] = []

        soup = BeautifulSoup(annotation_file, features="xml")
        sentence_tags = self._extract_sentence_tags(soup)
        math_entity_tags = self._extract_math_entity_tags(soup, error_messages)
        math_entities = self._construct_math_entities(
            math_entity_tags, sentence_tags, error_messages
        )

        logger.info("Loading math entities to database.")
        self._math_annotation_adapter.put_math_entities(
            transcript_id=transcript_id, math_entities=math_entities
        )

        return error_messages

    def _extract_sentence_tags(self, soup: BeautifulSoup) -> list[SentenceXMLTag]:
        sentences = []

        sentence_elements = soup.find_all("type5:Sentence")
        logger.info(
            f"Parsing {len(sentence_elements)} found 'type5:Sentence' elements."
        )
        for sentence in sentence_elements:
            try:
                sentences.append(
                    SentenceXMLTag(
                        xmi_id=sentence["xmi:id"],  # type: ignore
                        begin=int(sentence["begin"]),  # type: ignore
                        end=int(sentence["end"]),  # type: ignore
                    )
                )
            except Exception as e:
                raise ParseError(f"Failed to parse sentence element: {sentence}") from e

        logger.info(f"{len(sentences)} sentence elements parsed.")
        return sentences

    def _extract_math_entity_tags(
        self, soup: BeautifulSoup, error_messages: list[str]
    ) -> list[MathEntityXMLTag]:
        math_entities = []

        math_entity_elements = soup.find_all("custom:Math_entities")
        logger.info(
            f"Parsing {len(math_entity_elements)} found 'custom:Math_entities' elements."
        )
        for math_entity in math_entity_elements:
            try:
                math_entities.append(
                    MathEntityXMLTag(
                        xmi_id=math_entity["xmi:id"],  # type: ignore
                        begin=int(math_entity["begin"]),  # type: ignore
                        end=int(math_entity["end"]),  # type: ignore
                        math_tag=math_entity["math_tag"],  # type: ignore
                    )
                )
            except Exception as e:
                msg = f"Failed to parse math entity element: {math_entity}"
                logger.opt(exception=e).warning(msg)
                error_messages.append(msg)

        logger.debug(f"{len(math_entities)} math entity elements parsed.")
        return math_entities

    def _construct_math_entities(
        self,
        math_entity_tags: list[MathEntityXMLTag],
        sentence_tags: list[SentenceXMLTag],
        error_messages: list[str],
    ) -> list[MathEntityPutModel]:
        logger.info("Constructing MathEntity models.")
        math_entities = []
        sentences_start = [sent.begin for sent in sentence_tags]
        sentences_end = [sent.end for sent in sentence_tags]

        for math_entity_tag in math_entity_tags:
            try:
                sent_idx = bisect_left(sentences_end, math_entity_tag.begin)
                relative_start = math_entity_tag.begin - sentences_start[sent_idx]
                relative_end = math_entity_tag.end - sentences_start[sent_idx]
                math_entities.append(
                    MathEntityPutModel(
                        math_tag_id=math_entity_tag.math_tag.removeprefix(
                            self._inception_tag_prefix
                        ),
                        span=AnnotationSpanPutModel(
                            sent_idx=sent_idx,
                            char_start=relative_start,
                            char_end=relative_end,
                        ),
                    )
                )
            except Exception as e:
                msg = f"Failed to create MathEntity from xml tag: {math_entity_tag}"
                logger.opt(exception=e).warning(msg)
                error_messages.append(msg)
        return math_entities
