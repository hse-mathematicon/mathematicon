from pathlib import Path
from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, status
from loguru import logger
from yaml import safe_load
from yaml.parser import ParserError

from app.container import AppContainer
from app.domain.entities.transcripts import (
    TranscriptGetFiltersModel,
    TranscriptInfoModel,
    TranscriptUploadModel,
)
from app.infra.adapters.storage.transripts import TranscriptsAdapter

router = APIRouter(prefix="/transcripts", tags=["transcripts"])


@router.post("/uploadfile")
@inject
def upload_transcript_file(
    file: UploadFile,
    transcripts_adapter: Annotated[
        TranscriptsAdapter, Depends(Provide[AppContainer.transcripts_adapter])
    ],
) -> int:
    try:
        data = safe_load(file.file)
    except ParserError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Invalid YAML"
        ) from e

    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Can't retrieve filename.",
        )
    filename = Path(file.filename).stem

    logger.debug(f"filename: {filename}, fields: {list(data.keys())}")
    try:
        transcript = TranscriptUploadModel(
            filename=filename,
            src_url=data["yb_link"],
            title=data["title"],
            math_branch=data["branch"],
            difficulty=data["level"],
            timecode_start=data["timecode_start"],
            timecode_end=data["timecode_end"],
            text=data["text"],
        )
    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"Missing required field: {e}",
        ) from e
    return transcripts_adapter.add_transcript(transcript)


@router.get("/{id}/info")
@inject
def get_transcript_info(
    id: int,
    transcripts_adapter: Annotated[
        TranscriptsAdapter, Depends(Provide[AppContainer.transcripts_adapter])
    ],
) -> TranscriptInfoModel:
    transcript = transcripts_adapter.get_transcript_info(id)
    if not transcript:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return transcript


@router.get("/info")
@inject
def get_transcripts_info_by_filters(
    filters: Annotated[TranscriptGetFiltersModel, Query()],
    transcripts_adapter: Annotated[
        TranscriptsAdapter, Depends(Provide[AppContainer.transcripts_adapter])
    ],
) -> list[TranscriptInfoModel]:
    return transcripts_adapter.get_transcripts_info_by_filters(filters=filters)


@router.delete("/{id}")
@inject
def delete_transcript(
    id: int,
    transcripts_adapter: Annotated[
        TranscriptsAdapter, Depends(Provide[AppContainer.transcripts_adapter])
    ],
) -> None:
    transcripts_adapter.delete_transcript(id)
