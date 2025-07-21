from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from workout_api.models.centro_treinamento_model import CentroTreinamentoModel
from workout_api.schemas.centro_treinamento_schema import CentroTreinamentoIn, CentroTreinamentoOut

class CentroTreinamentoController:
    
    @staticmethod
    async def create(db_session: AsyncSession, centro_in: CentroTreinamentoIn) -> CentroTreinamentoOut:
        centro_out = CentroTreinamentoModel(**centro_in.model_dump())
        db_session.add(centro_out)
        
        try:
            await db_session.commit()
            await db_session.refresh(centro_out)
        except IntegrityError:
            await db_session.rollback()
            raise HTTPException(
                status_code=303, 
                detail=f'Já existe um centro de treinamento cadastrado com o nome: {centro_in.nome}'
            )
        
        return centro_out
    
    @staticmethod
    async def get_all(db_session: AsyncSession) -> list[CentroTreinamentoOut]:
        statement = select(CentroTreinamentoModel)
        result = await db_session.execute(statement)
        return result.scalars().all()
    
    @staticmethod
    async def get_by_id(db_session: AsyncSession, id: int) -> CentroTreinamentoOut:
        statement = select(CentroTreinamentoModel).filter(CentroTreinamentoModel.pk_id == id)
        result = await db_session.execute(statement)
        centro = result.scalar_one_or_none()
        
        if not centro:
            raise HTTPException(status_code=404, detail=f'Centro de treinamento com id {id} não encontrado')
        
        return centro 