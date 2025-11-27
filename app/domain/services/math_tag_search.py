from collections import defaultdict
from dataclasses import dataclass
from typing import Optional

from loguru import logger

from app.domain.entities.math_annotation import MathEntityGetFilterModel
from app.domain.entities.search import (
    MathTagSentenceMatchInfo,
    SearchResultSentenceInfo,
    SearchResultTranscriptInfo,
)
from app.domain.entities.sentences import SentenceFilterModel, SentenceInfoModel
from app.domain.services.interfaces.math_annotation import MathAnnotationInterface
from app.domain.services.interfaces.math_ontology import MathOntologyInterface
from app.domain.services.interfaces.sentences import SentencesInterface
from app.domain.services.interfaces.transcripts import TranscriptsInterface


@dataclass
class MathTagSearchService:
    _transcripts_adapter: TranscriptsInterface
    _sentences_adapter: SentencesInterface
    _ontology_adapter: MathOntologyInterface
    _math_annotation_adapter: MathAnnotationInterface

    def search(self, math_tag_id: str) -> list[MathTagSentenceMatchInfo]:
        math_tags = [math_tag_id] + self._ontology_adapter.get_tag_descendants(
            math_tag_id
        )
        math_entities = self._math_annotation_adapter.get_math_entities(
            MathEntityGetFilterModel(math_tag_id_in=math_tags)
        )

        math_entities_by_sent = defaultdict(list)
        for ent in math_entities:
            math_entities_by_sent[ent.sent_id].append(ent)

        sentences = {}
        transcripts_info = {}
        for sent_id in math_entities_by_sent:
            sentence = self._sentences_adapter.get_sentence(sent_id)
            if sentence is None:
                logger.warning(f"Failed to get {sent_id=}")
                continue

            if sentence.transcript_id not in transcripts_info:
                transcript_info = self._create_search_result_transcript_info(
                    sentence.transcript_id
                )
                if transcript_info is None:
                    logger.warning(f"Failed to get {transcript_info=}")
                    continue
                transcripts_info[sent_id] = transcript_info

            sentences[sent_id] = sentence

        result = []
        for sent_id in sentences:
            result.append(
                MathTagSentenceMatchInfo(
                    transcript_info=transcripts_info[sent_id],
                    sent_info=self._create_search_result_sentence_info(
                        sentences[sent_id]
                    ),
                    math_entities=math_entities_by_sent[sent_id],
                )
            )
        return result

    def _create_search_result_sentence_info(
        self, sentence: SentenceInfoModel
    ) -> SearchResultSentenceInfo:
        prev_sentence = self._sentences_adapter.get_sentences(
            SentenceFilterModel(
                transcript_id=sentence.transcript_id, position=sentence.position - 1
            )
        )
        next_sentence = self._sentences_adapter.get_sentences(
            SentenceFilterModel(
                transcript_id=sentence.transcript_id, position=sentence.position + 1
            )
        )
        return SearchResultSentenceInfo(
            sent_id=sentence.id,
            tokens=self._sentences_adapter.get_sentence_tokens(sentence.id),
            left_context=prev_sentence[0].text if prev_sentence else None,
            right_context=next_sentence[0].text if next_sentence else None,
            timecode_start=sentence.timecode_start,
        )

    def _create_search_result_transcript_info(
        self, transcript_id: int
    ) -> Optional[SearchResultTranscriptInfo]:
        transcript = self._transcripts_adapter.get_transcript_info(transcript_id)
        return (
            SearchResultTranscriptInfo(src_url=transcript.src_url)
            if transcript
            else None
        )
