from typing import List
from sqlalchemy.orm import Session

from app.domain.entities.morphology import POSTagModel
from app.domain.repositories.morphology import IPOSTagRepository
from app.infra.db.models.morphology import POSTagDBModel

class POSTagAdapter(IPOSTagRepository):
    """Адаптер для работы с частеречными тегами в базе данных"""
    
    def __init__(self, _db_engine):  # ← меняем на _db_engine
        self.session = Session(_db_engine)  # ← создаем сессию из engine
    
    def get_all(self) -> List[POSTagModel]:
        """Получить все частеречные теги из базы данных"""
        db_tags = self.session.query(POSTagDBModel).all()
        
        return [
            POSTagModel(
                tag=tag.tag,
                info_url=tag.info_url or "",
                name_ru=tag.name_ru,
                name_en=tag.name_en,
                examples=tag.examples or ""
            )
            for tag in db_tags
        ]