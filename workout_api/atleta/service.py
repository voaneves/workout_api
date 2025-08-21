from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from workout_api.atleta.models import AtletaModel
from workout_api.atleta.schemas import AtletaIn, AtletaOut, AtletaUpdate
from workout_api.categorias.models import CategoriaModel
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.contrib.dependencies import DatabaseDependency


class AtletaService:
    @staticmethod
    async def create(db_session: DatabaseDependency, atleta_in: AtletaIn) -> AtletaOut:
        # Verifica se a categoria e o centro de treinamento existem
        categoria_nome = atleta_in.categoria.nome
        centro_treinamento_nome = atleta_in.centro_treinamento.nome

        categoria = (await db_session.execute(
            select(CategoriaModel).filter_by(nome=categoria_nome))
        ).scalars().first()

        if not categoria:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'A categoria {categoria_nome} não foi encontrada.'
            )

        centro_treinamento = (await db_session.execute(
            select(CentroTreinamentoModel).filter_by(nome=centro_treinamento_nome))
        ).scalars().first()

        if not centro_treinamento:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'O centro de treinamento {centro_treinamento_nome} não foi encontrado.'
            )
        
        # Tenta criar o atleta
        try:
            atleta_out = AtletaOut(id=uuid4(), created_at=datetime.utcnow(), **atleta_in.model_dump())
            atleta_model = AtletaModel(**atleta_out.model_dump(exclude={'categoria', 'centro_treinamento'}))
            
            atleta_model.categoria_id = categoria.pk_id
            atleta_model.centro_treinamento_id = centro_treinamento.pk_id
            
            db_session.add(atleta_model)
            await db_session.commit()
            await db_session.refresh(atleta_model)

        # Captura o erro de integridade (CPF duplicado)
        except IntegrityError:
            await db_session.rollback()
            raise HTTPException(
                status_code=status.HTTP_303_SEE_OTHER,
                detail=f"Já existe um atleta cadastrado com o cpf: {atleta_in.cpf}"
            )
        
        # Associa os objetos completos para o retorno
        # (O refresh não carrega relacionamentos automaticamente)
        atleta_out.categoria = categoria
        atleta_out.centro_treinamento = centro_treinamento
        
        return atleta_out

    @staticmethod
    async def get(db_session: DatabaseDependency, id: str) -> AtletaOut:
        atleta: AtletaOut | None = (
            await db_session.execute(select(AtletaModel).filter_by(id=id))
        ).scalars().first()

        if not atleta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Atleta não encontrado com id: {id}'
            )
        
        return atleta

    @staticmethod
    async def query(db_session: DatabaseDependency, nome: Optional[str] = None, cpf: Optional[str] = None) -> List[AtletaOut]:
        query = select(AtletaModel)
        
        if nome:
            query = query.filter(AtletaModel.nome == nome)
        if cpf:
            query = query.filter(AtletaModel.cpf == cpf)
        
        atletas: List[AtletaOut] = (await db_session.execute(query)).scalars().all()
        
        return atletas

    @staticmethod
    async def update(db_session: DatabaseDependency, id: str, atleta_up: AtletaUpdate) -> AtletaOut:
        atleta: AtletaOut | None = (
            await db_session.execute(select(AtletaModel).filter_by(id=id))
        ).scalars().first()

        if not atleta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Atleta não encontrado com id: {id}'
            )
        
        atleta_update_data = atleta_up.model_dump(exclude_unset=True)
        for key, value in atleta_update_data.items():
            setattr(atleta, key, value)
            
        await db_session.commit()
        await db_session.refresh(atleta)
        
        return atleta

    @staticmethod
    async def delete(db_session: DatabaseDependency, id: str) -> None:
        atleta: AtletaOut | None = (
            await db_session.execute(select(AtletaModel).filter_by(id=id))
        ).scalars().first()

        if not atleta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Atleta não encontrado com id: {id}'
            )
        
        await db_session.delete(atleta)
        await db_session.commit()
