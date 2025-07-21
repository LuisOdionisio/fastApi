from fastapi import APIRouter, Body, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from workout_api.configs.database import get_session
from workout_api.controllers.centro_treinamento_controller import CentroTreinamentoController
from workout_api.schemas.centro_treinamento_schema import CentroTreinamentoIn, CentroTreinamentoOut

router = APIRouter()

@router.post(
    '/', 
    summary='Criar um novo centro de treinamento',
    status_code=status.HTTP_201_CREATED,
    response_model=CentroTreinamentoOut
)
async def post(
    centro_in: CentroTreinamentoIn = Body(...),
    db_session: AsyncSession = Depends(get_session)
) -> CentroTreinamentoOut:
    return await CentroTreinamentoController.create(db_session=db_session, centro_in=centro_in)

@router.get(
    '/', 
    summary='Consultar todos os centros de treinamento',
    status_code=status.HTTP_200_OK,
    response_model=list[CentroTreinamentoOut]
)
async def query(
    db_session: AsyncSession = Depends(get_session)
) -> list[CentroTreinamentoOut]:
    return await CentroTreinamentoController.get_all(db_session=db_session)

@router.get(
    '/{id}', 
    summary='Consultar um centro de treinamento pelo id',
    status_code=status.HTTP_200_OK,
    response_model=CentroTreinamentoOut
)
async def get(
    id: int,
    db_session: AsyncSession = Depends(get_session)
) -> CentroTreinamentoOut:
    return await CentroTreinamentoController.get_by_id(db_session=db_session, id=id) 