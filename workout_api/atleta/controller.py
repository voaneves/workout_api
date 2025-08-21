from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from fastapi_pagination import Page, paginate
from pydantic import UUID4

from workout_api.atleta.models import AtletaModel
from workout_api.atleta.schemas import (AtletaCustom, AtletaIn, AtletaOut,
                                       AtletaUpdate)
from workout_api.atleta.service import AtletaService
from workout_api.contrib.dependencies import DatabaseDependency

router = APIRouter(prefix='/atletas', tags=['atleta'])


@router.post(
    '/',
    summary='Criar um novo atleta',
    status_code=status.HTTP_201_CREATED,
    response_model=AtletaOut
)
async def post(
    db_session: DatabaseDependency,
    atleta_in: AtletaIn = Body(...),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Cria um novo atleta na base de dados.
    Apenas usuários autenticados podem criar atletas.
    """
    try:
        return await AtletaService.create(db_session=db_session, atleta_in=atleta_in)
    except Exception as e:
        raise e


@router.get(
    '/',
    summary='Consultar todos os atletas',
    status_code=status.HTTP_200_OK,
    response_model=Page[AtletaCustom],
)
async def query(
    db_session: DatabaseDependency,
    nome: Optional[str] = Query(None, description="Filtrar por nome do atleta"),
    cpf: Optional[str] = Query(None, description="Filtrar por CPF do atleta")
) -> Page[AtletaCustom]:
    atletas: List[AtletaOut] = await AtletaService.query(db_session=db_session, nome=nome, cpf=cpf)
    atletas_custom = [
        AtletaCustom(
            nome=atleta.nome,
            centro_treinamento=atleta.centro_treinamento.nome,
            categoria=atleta.categoria.nome
        ) for atleta in atletas
    ]
    return paginate(atletas_custom)


@router.get(
    '/{id}',
    summary='Consultar um atleta pelo id',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def get(id: UUID4, db_session: DatabaseDependency) -> AtletaOut:
    return await AtletaService.get(db_session=db_session, id=id)


@router.patch(
    '/{id}',
    summary='Editar um atleta pelo id',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def patch(id: UUID4, db_session: DatabaseDependency, atleta_up: AtletaUpdate = Body(...)) -> AtletaOut:
    return await AtletaService.update(db_session=db_session, id=id, atleta_up=atleta_up)


@router.delete(
    '/{id}',
    summary='Deletar um atleta pelo id',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete(id: UUID4, db_session: DatabaseDependency) -> None:
    await AtletaService.delete(db_session=db_session, id=id)
