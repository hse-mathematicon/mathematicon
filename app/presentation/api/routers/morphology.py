from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from app.container import AppContainer
from app.domain.entities.morphology import POSTagModel
from app.domain.repositories.morphology import IPOSTagRepository

router = APIRouter(prefix="/morphology", tags=["morphology"])

@router.get("/pos-tags", response_model=list[POSTagModel])
@inject
def get_pos_tags(
    pos_tag_repo: IPOSTagRepository = Depends(Provide[AppContainer.pos_tag_adapter])
) -> list[POSTagModel]:
    """
    Получить список всех частеречных тегов
    """
    return pos_tag_repo.get_all()