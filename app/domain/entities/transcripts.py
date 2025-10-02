from typing import Optional

from pydantic import BaseModel, ConfigDict


class TranscriptUploadModel(BaseModel):
    filename: str
    src_url: str
    title: str
    math_branch: str
    difficulty: str
    timecode_start: str
    timecode_end: str
    text: str


class TranscriptInfoModel(BaseModel):
    id: int
    filename: str
    src_url: str
    title: str
    math_branch: str
    difficulty: str
    timecode_start: str
    timecode_end: str

    model_config = ConfigDict(from_attributes=True)


class TranscriptGetFiltersModel(BaseModel):
    filename: Optional[str] = None
    src_url: Optional[str] = None
