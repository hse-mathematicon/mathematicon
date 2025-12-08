from io import StringIO
from typing import Annotated, Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse

from app.container import AppContainer
from app.domain.entities.sentences import GrammarAnnotationStatsModel
from app.domain.services.grammar_annotation_service import GrammarAnnotationService
from app.infra.adapters.storage.sentences import SentencesAdapter
from app.infra.adapters.storage.transripts import TranscriptsAdapter

router = APIRouter(prefix="/grammar_annotation", tags=["grammar_annotation"])


@router.post("/{transcript_id}/generate", status_code=status.HTTP_204_NO_CONTENT)
@inject
def parse_transcript(
    transcript_id: int,
    grammar_annotation_service: Annotated[
        GrammarAnnotationService,
        Depends(Provide[AppContainer.grammar_annotation_service]),
    ],
) -> None:
    grammar_annotation_service.parse(transcript_id)


@router.get(
    "/{transcript_id}/conllu",
    response_class=StreamingResponse,
    responses={status.HTTP_404_NOT_FOUND: {"description": "Transcript not found."}},
)
@inject
def get_transcript_conllu(
    transcript_id: int,
    transcripts_adapter: Annotated[
        TranscriptsAdapter, Depends(Provide[AppContainer.transcripts_adapter])
    ],
    grammar_annotation_service: Annotated[
        GrammarAnnotationService,
        Depends(Provide[AppContainer.grammar_annotation_service]),
    ],
) -> StreamingResponse:
    transcript_info = transcripts_adapter.get_transcript_info(transcript_id)
    if not transcript_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    conll_str = grammar_annotation_service.get_conllu(transcript_id)
    filename = f"{transcript_info.filename}.conllu"
    return StreamingResponse(
        content=StringIO(conll_str),
        media_type="text/plain",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@router.delete("/{transcript_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
def delete_transcript_grammar_annotation(
    transcript_id: int,
    sentences_adapter: Annotated[
        SentencesAdapter, Depends(Provide[AppContainer.sentences_adapter])
    ],
) -> None:
    sentences_adapter.delete_sentences(transcript_id)


@router.get(
    "/{transcript_id}/stats",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_404_NOT_FOUND: {"description": "Transcript not found."}},
)
@inject
def get_grammar_annotation_stats(
    transcript_id: int,
    transcripts_adapter: Annotated[
        TranscriptsAdapter, Depends(Provide[AppContainer.transcripts_adapter])
    ],
    sentences_adapter: Annotated[
        SentencesAdapter, Depends(Provide[AppContainer.sentences_adapter])
    ],
) -> Optional[GrammarAnnotationStatsModel]:
    transcript_info = transcripts_adapter.get_transcript_info(transcript_id)
    if not transcript_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return sentences_adapter.get_grammar_annotation_stats(transcript_id)
