from pydantic import BaseModel

class POSTagModel(BaseModel):
    """Pydantic модель для возврата данных через API"""
    tag: str
    info_url: str
    name_ru: str
    name_en: str
    examples: str
    
    class Config:
        from_attributes = True