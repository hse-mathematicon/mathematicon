from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.morphology import POSTagModel

class IPOSTagRepository(ABC):
    """Интерфейс репозитория для работы с частеречными тегами"""
    
    @abstractmethod
    def get_all(self) -> List[POSTagModel]:
        """Получить все частеречные теги"""
        pass