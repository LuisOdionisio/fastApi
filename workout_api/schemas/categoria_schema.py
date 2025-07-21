from pydantic import BaseModel, Field
from typing import Annotated

class CategoriaIn(BaseModel):
    nome: Annotated[str, Field(description='Nome da categoria', example='Scale', max_length=50)]

class CategoriaOut(CategoriaIn):
    pk_id: Annotated[int, Field(description='Identificador da categoria')] 