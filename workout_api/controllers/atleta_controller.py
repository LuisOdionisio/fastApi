from datetime import datetime
from uuid import uuid4
from fastapi import HTTPException
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Page
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from workout_api.models.atleta_model import AtletaModel
from workout_api.schemas.atleta_schema import AtletaIn, AtletaOut, AtletaUpdate, AtletaListOut

class AtletaController:
    
    @staticmethod
    async def create(db_session: AsyncSession, atleta_in: AtletaIn) -> AtletaOut:
        atleta_out = AtletaModel(created_at=datetime.utcnow(), **atleta_in.model_dump())
        db_session.add(atleta_out)
        
        try:
            await db_session.commit()
            await db_session.refresh(atleta_out)
        except IntegrityError:
            await db_session.rollback()
            raise HTTPException(
                status_code=303, 
                detail=f'Já existe um atleta cadastrado com o cpf: {atleta_in.cpf}'
            )
        
        return atleta_out
    
    @staticmethod
    async def get_all(
        db_session: AsyncSession,
        nome: str = None,
        cpf: str = None
    ) -> Page[AtletaListOut]:
        statement = select(AtletaModel)
        
        if nome:
            statement = statement.filter(AtletaModel.nome.ilike(f'%{nome}%'))
        if cpf:
            statement = statement.filter(AtletaModel.cpf == cpf)
        
        # Paginação com fastapi-pagination
        result = await paginate(db_session, statement)
        
        # Customizar os items retornados para incluir apenas nome, centro_treinamento, categoria
        custom_items = [
            AtletaListOut(
                nome=atleta.nome,
                centro_treinamento=atleta.centro_treinamento,
                categoria=atleta.categoria
            ) 
            for atleta in result.items
        ]
        
        # Retorna página com items customizados
        return Page.create(
            items=custom_items,
            total=result.total,
            params=result.__params__
        )
    
    @staticmethod
    async def get_by_id(db_session: AsyncSession, id: int) -> AtletaOut:
        statement = select(AtletaModel).filter(AtletaModel.pk_id == id)
        result = await db_session.execute(statement)
        atleta = result.scalar_one_or_none()
        
        if not atleta:
            raise HTTPException(status_code=404, detail=f'Atleta com id {id} não encontrado')
        
        return atleta
    
    @staticmethod
    async def update(db_session: AsyncSession, id: int, atleta_update: AtletaUpdate) -> AtletaOut:
        statement = select(AtletaModel).filter(AtletaModel.pk_id == id)
        result = await db_session.execute(statement)
        atleta = result.scalar_one_or_none()
        
        if not atleta:
            raise HTTPException(status_code=404, detail=f'Atleta com id {id} não encontrado')
        
        atleta_data = atleta_update.model_dump(exclude_unset=True)
        for key, value in atleta_data.items():
            setattr(atleta, key, value)
        
        await db_session.commit()
        await db_session.refresh(atleta)
        
        return atleta
    
    @staticmethod
    async def delete(db_session: AsyncSession, id: int) -> None:
        statement = select(AtletaModel).filter(AtletaModel.pk_id == id)
        result = await db_session.execute(statement)
        atleta = result.scalar_one_or_none()
        
        if not atleta:
            raise HTTPException(status_code=404, detail=f'Atleta com id {id} não encontrado')
        
        await db_session.delete(atleta)
        await db_session.commit() 