from sqlalchemy import Column, Integer, String
from workout_api.configs.database import BaseModel

class CategoriaModel(BaseModel):
    __tablename__ = 'categorias'
    
    pk_id = Column(Integer, primary_key=True)
    nome = Column(String(50), unique=True, nullable=False) 