from pydantic import BaseModel, Field, validator
from typing import Annotated, Optional
from datetime import datetime
from workout_api.schemas.categoria_schema import CategoriaOut
from workout_api.schemas.centro_treinamento_schema import CentroTreinamentoOut

class AtletaIn(BaseModel):
    nome: Annotated[str, Field(description='Nome do atleta', example='João', max_length=50)]
    cpf: Annotated[str, Field(description='CPF do atleta', example='12345678901', max_length=11, min_length=11)]
    idade: Annotated[int, Field(description='Idade do atleta', example=25, gt=0)]
    peso: Annotated[float, Field(description='Peso do atleta', example=75.5, gt=0)]
    altura: Annotated[float, Field(description='Altura do atleta', example=1.70, gt=0)]
    sexo: Annotated[str, Field(description='Sexo do atleta', example='M', max_length=1)]
    categoria_id: Annotated[int, Field(description='Identificador da categoria')]
    centro_treinamento_id: Annotated[int, Field(description='Identificador do centro de treinamento')]
    
    @validator('cpf')
    def validate_cpf(cls, v):
        if not v.isdigit():
            raise ValueError('CPF deve conter apenas números')
        return v
    
    @validator('sexo')
    def validate_sexo(cls, v):
        if v.upper() not in ['M', 'F']:
            raise ValueError('Sexo deve ser M ou F')
        return v.upper()

class AtletaOut(AtletaIn):
    pk_id: Annotated[int, Field(description='Identificador do atleta')]
    created_at: Annotated[datetime, Field(description='Data de criação')]
    categoria: CategoriaOut
    centro_treinamento: CentroTreinamentoOut

class AtletaUpdate(BaseModel):
    nome: Annotated[Optional[str], Field(None, description='Nome do atleta', example='João', max_length=50)]
    idade: Annotated[Optional[int], Field(None, description='Idade do atleta', example=25, gt=0)]

# Schema customizado para listagem (get all) - apenas nome, centro_treinamento e categoria
class AtletaListOut(BaseModel):
    nome: Annotated[str, Field(description='Nome do atleta')]
    centro_treinamento: CentroTreinamentoOut
    categoria: CategoriaOut 