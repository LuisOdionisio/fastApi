from pydantic import BaseModel, Field
from typing import Annotated

class CentroTreinamentoIn(BaseModel):
    nome: Annotated[str, Field(description='Nome do centro de treinamento', example='CT King', max_length=50)]
    endereco: Annotated[str, Field(description='Endereço do centro de treinamento', example='Rua X, 123', max_length=60)]
    proprietario: Annotated[str, Field(description='Proprietário do centro de treinamento', example='Marcos', max_length=30)]

class CentroTreinamentoOut(CentroTreinamentoIn):
    pk_id: Annotated[int, Field(description='Identificador do centro de treinamento')] 