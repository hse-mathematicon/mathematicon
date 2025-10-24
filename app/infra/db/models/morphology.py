from sqlalchemy import Column, Integer, String, Text
from app.infra.db.models.base import BaseModel  

class POSTagDBModel(BaseModel):  
    """Модель для хранения частеречных тегов в базе данных"""
    
    __tablename__ = "pos_tags"
    
    id = Column(Integer, primary_key=True, index=True)
    tag = Column(String(10), unique=True, nullable=False, index=True)
    info_url = Column(String(500), nullable=True)
    name_ru = Column(String(100), nullable=False)
    name_en = Column(String(100), nullable=False)
    examples = Column(Text, nullable=True)