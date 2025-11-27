from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.container import AppContainer
from app.domain.services.math_tag_search import MathTagSearchService
from app.presentation.api.schemas.search import MathTagSearchResult

router = APIRouter(prefix="/search", tags=["search"])


@router.get("/math-tag")
@inject
def math_tag_search(
    math_tag_id: str,
    math_tag_search_service: Annotated[
        MathTagSearchService, Depends(Provide[AppContainer.math_tag_search_service])
    ],
) -> MathTagSearchResult:
    result = math_tag_search_service.search(math_tag_id)
    return MathTagSearchResult(
        query=math_tag_id,
        result=result,
        total=len(result),
    )
