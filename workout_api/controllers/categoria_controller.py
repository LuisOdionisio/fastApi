from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from workout_api.models.categoria_model import CategoriaModel
from workout_api.schemas.categoria_schema import CategoriaIn, CategoriaOut

class CategoriaController:
    
    @staticmethod
    async def create(db_session: AsyncSession, categoria_in: CategoriaIn) -> CategoriaOut:
        categoria_out = CategoriaModel(**categoria_in.model_dump())
        db_session.add(categoria_out)
        
        try:
            await db_session.commit()
            await db_session.refresh(categoria_out)
        except IntegrityError:
            await db_session.rollback()
            raise HTTPException(
                status_code=303, 
                detail=f'Já existe uma categoria cadastrada com o nome: {categoria_in.nome}'
            )
        
        return categoria_out
    
    @staticmethod
    async def get_all(db_session: AsyncSession) -> list[CategoriaOut]:
        statement = select(CategoriaModel)
        result = await db_session.execute(statement)
        return result.scalars().all()
    
    @staticmethod
    async def get_by_id(db_session: AsyncSession, id: int) -> CategoriaOut:
        statement = select(CategoriaModel).filter(CategoriaModel.pk_id == id)
        result = await db_session.execute(statement)
        categoria = result.scalar_one_or_none()
        
        if not categoria:
            raise HTTPException(status_code=404, detail=f'Categoria com id {id} não encontrada')
        
        return categoria 