from fastapi import APIRouter, Body, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from workout_api.configs.database import get_session
from workout_api.controllers.categoria_controller import CategoriaController
from workout_api.schemas.categoria_schema import CategoriaIn, CategoriaOut

router = APIRouter()

@router.post(
    '/', 
    summary='Criar uma nova categoria',
    status_code=status.HTTP_201_CREATED,
    response_model=CategoriaOut
)
async def post(
    categoria_in: CategoriaIn = Body(...),
    db_session: AsyncSession = Depends(get_session)
) -> CategoriaOut:
    return await CategoriaController.create(db_session=db_session, categoria_in=categoria_in)

@router.get(
    '/', 
    summary='Consultar todas as categorias',
    status_code=status.HTTP_200_OK,
    response_model=list[CategoriaOut]
)
async def query(
    db_session: AsyncSession = Depends(get_session)
) -> list[CategoriaOut]:
    return await CategoriaController.get_all(db_session=db_session)

@router.get(
    '/{id}', 
    summary='Consultar uma categoria pelo id',
    status_code=status.HTTP_200_OK,
    response_model=CategoriaOut
)
async def get(
    id: int,
    db_session: AsyncSession = Depends(get_session)
) -> CategoriaOut:
    return await CategoriaController.get_by_id(db_session=db_session, id=id) 