from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, UploadFile, status

from app.container import AppContainer
from app.domain.entities.math_annotation import MathEntityGetFilterModel
from app.domain.services.math_annotation_service import MathAnnotationService
from app.infra.adapters.storage.math_annotation import MathAnnotationAdapter

router = APIRouter(prefix="/math_annotation", tags=["math_annotation"])


@router.post(
    "/{transcript_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_409_CONFLICT: {"description": "Math annotation already exists."}
    },
)
@inject
def upload_xmi(
    transcript_id: int,
    xmi_file: UploadFile,
    math_annotation_adapter: Annotated[
        MathAnnotationAdapter, Depends(Provide[AppContainer.math_annotation_adapter])
    ],
    math_annotation_service: Annotated[
        MathAnnotationService, Depends(Provide[AppContainer.math_annotation_service])
    ],
) -> None:
    if math_annotation_adapter.check_math_entities_exist(
        MathEntityGetFilterModel(transcript_id=transcript_id)
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Math annotation for {transcript_id=} already exists.",
        )
    math_annotation_service.load_math_annotation(transcript_id, xmi_file.file)


@router.delete("/{transcript_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
def delete_trasncript_math_annotation(
    transcript_id: int,
    math_annotation_adapter: Annotated[
        MathAnnotationAdapter, Depends(Provide[AppContainer.math_annotation_adapter])
    ],
) -> None:
    math_annotation_adapter.delete_math_entities(transcript_id)
