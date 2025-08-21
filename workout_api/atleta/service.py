from typing import List, Optional
from fastapi import Depends
from sqlalchemy.future import select
from workout_api.atleta.models import AtletaModel
from workout_api.atleta.schemas import AtletaOut
from workout_api.contrib.dependencies import DatabaseDependency

class AtletaService:
    @staticmethod
    async def query(
        db_session: DatabaseDependency,
        nome: Optional[str] = None,
        cpf: Optional[str] = None
    ) -> List[AtletaOut]:
        query = select(AtletaModel)
        if nome:
            query = query.filter(AtletaModel.nome == nome)
        if cpf:
            query = query.filter(AtletaModel.cpf == cpf)

        atletas: List[AtletaOut] = (await db_session.execute(query)).scalars().all()
        return atletas
