from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, UploadFile, status

from app.container import AppContainer
from app.domain.services.math_ontology_service import MathOntologyService
from app.infra.adapters.storage.math_ontology import MathOntologyAdapter

router = APIRouter(prefix="/math_ontology", tags=["math_ontology"])


@router.post("/upload_rdf", status_code=status.HTTP_204_NO_CONTENT)
@inject
def upload_rdf(
    rdf: UploadFile,
    math_ontology_service: Annotated[
        MathOntologyService, Depends(Provide[AppContainer.math_ontology_service])
    ],
) -> None:
    math_ontology_service.load_from_rdf(rdf.file)


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
@inject
def delete_math_ontology(
    math_ontology_adapter: Annotated[
        MathOntologyAdapter, Depends(Provide[AppContainer.math_ontology_adapter])
    ],
) -> None:
    math_ontology_adapter.delete_math_ontology()
