from abc import abstractmethod
from typing import Protocol


class TranscriptsInterface(Protocol):
    @abstractmethod
    def get_transcript_text(self, transcript_id: int) -> str: ...
