from dataclasses import dataclass

from app.domain.services.interfaces.language_parser import LanguageParserInterface
from app.domain.services.interfaces.sentences import SentencesInterface
from app.domain.services.interfaces.transcripts import TranscriptsInterface


@dataclass
class GrammarAnnotationService:
    _language_parser: LanguageParserInterface
    _transcripts_adapter: TranscriptsInterface
    _sentences_adapter: SentencesInterface

    def parse(self, transcript_id: int) -> None:
        text = self._transcripts_adapter.get_transcript_text(transcript_id)
        parsed = self._language_parser.parse(text)
        for sent in parsed:
            self._sentences_adapter.put_sentence(transcript_id, sent)

    def get_conllu(self, transcript_id: int) -> str:
        text = self._transcripts_adapter.get_transcript_text(transcript_id)
        return self._language_parser.generate_conllu(text)
