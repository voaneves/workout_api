from fastapi import APIRouter
from workout_api.atleta.controller import router as atleta
from workout_api.categoria.controller import router as categoria
from workout_api.centro_treinamento.controller import router as centro_treinamento
from workout_api.auth.controller import router as auth

api_router = APIRouter()
api_router.include_router(auth, prefix='/auth')
api_router.include_router(atleta, prefix='/atletas')
api_router.include_router(categoria, prefix='/categorias')
api_router.include_router(centro_treinamento, prefix='/centros_treinamento')
