from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Importa as configurações
from workout_api.configs.settings import settings

# Usa a variável correta: DATABASE_URL
engine = create_async_engine(settings.DATABASE_URL, echo=False)

# Renomeado para 'async_session_maker' para ficar mais claro que é um "fabricante" de sessões
async_session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    # Usa o 'async_session_maker' para criar a sessão
    async with async_session_maker() as session:
        yield session
