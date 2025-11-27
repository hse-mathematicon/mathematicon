from abc import abstractmethod
from typing import Optional, Protocol

from app.domain.entities.transcripts import (
    TranscriptInfoModel,
)


class TranscriptsInterface(Protocol):
    @abstractmethod
    def get_transcript_text(self, transcript_id: int) -> str: ...

    @abstractmethod
    def get_transcript_info(
        self, transcript_id: int
    ) -> Optional[TranscriptInfoModel]: ...
