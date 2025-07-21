from fastapi import APIRouter, Body, Depends, Query, status
from fastapi_pagination import Page
from sqlalchemy.ext.asyncio import AsyncSession
from workout_api.configs.database import get_session
from workout_api.controllers.atleta_controller import AtletaController
from workout_api.schemas.atleta_schema import AtletaIn, AtletaOut, AtletaUpdate, AtletaListOut

router = APIRouter()

@router.post(
    '/', 
    summary='Criar um novo atleta',
    status_code=status.HTTP_201_CREATED,
    response_model=AtletaOut
)
async def post(
    atleta_in: AtletaIn = Body(...),
    db_session: AsyncSession = Depends(get_session)
) -> AtletaOut:
    return await AtletaController.create(db_session=db_session, atleta_in=atleta_in)

@router.get(
    '/', 
    summary='Consultar todos os atletas',
    status_code=status.HTTP_200_OK,
    response_model=Page[AtletaListOut]
)
async def query(
    db_session: AsyncSession = Depends(get_session),
    nome: str = Query(None, description="Filtrar por nome do atleta"),
    cpf: str = Query(None, description="Filtrar por CPF do atleta")
) -> Page[AtletaListOut]:
    return await AtletaController.get_all(
        db_session=db_session, 
        nome=nome, 
        cpf=cpf
    )

@router.get(
    '/{id}', 
    summary='Consultar um atleta pelo id',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut
)
async def get(
    id: int,
    db_session: AsyncSession = Depends(get_session)
) -> AtletaOut:
    return await AtletaController.get_by_id(db_session=db_session, id=id)

@router.patch(
    '/{id}', 
    summary='Editar um atleta pelo id',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut
)
async def patch(
    id: int,
    atleta_update: AtletaUpdate = Body(...),
    db_session: AsyncSession = Depends(get_session)
) -> AtletaOut:
    return await AtletaController.update(
        db_session=db_session, 
        id=id, 
        atleta_update=atleta_update
    )

@router.delete(
    '/{id}', 
    summary='Deletar um atleta pelo id',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete(
    id: int,
    db_session: AsyncSession = Depends(get_session)
) -> None:
    return await AtletaController.delete(db_session=db_session, id=id) 