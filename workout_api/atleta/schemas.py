from typing import Annotated, Optional
from pydantic import Field, PositiveFloat
from workout_api.contrib.schemas import BaseSchema, OutMixin


# Schema para representar a categoria dentro do atleta (evita dependência circular)
class CategoriaIn(BaseSchema):
    nome: Annotated[str, Field(description='Nome da categoria', example='Scale', max_length=10)]


# Schema para representar o centro de treinamento dentro do atleta
class CentroTreinamentoIn(BaseSchema):
    nome: Annotated[str, Field(description='Nome do centro de treinamento', example='CT King', max_length=20)]


# Schema base com os campos comuns do atleta
class Atleta(BaseSchema):
    nome: Annotated[str, Field(description='Nome do atleta', example='Joao', max_length=50)]
    cpf: Annotated[str, Field(description='CPF do atleta', example='12345678900', max_length=11)]
    idade: Annotated[int, Field(description='Idade do atleta', example=25)]
    peso: Annotated[PositiveFloat, Field(description='Peso do atleta', example=75.5)]
    altura: Annotated[PositiveFloat, Field(description='Altura do atleta', example=1.80)]
    sexo: Annotated[str, Field(description='Sexo do atleta', example='M', max_length=1)]


# Schema para a criação de um novo atleta (entrada de dados na API)
class AtletaIn(Atleta):
    categoria: Annotated[CategoriaIn, Field(description='Categoria do atleta')]
    centro_treinamento: Annotated[CentroTreinamentoIn, Field(description='Centro de treinamento do atleta')]


# Schema para a representação de um atleta na saída da API (resposta da API)
# Herda os campos de 'Atleta' e os campos 'id' e 'created_at' do 'OutMixin'
class AtletaOut(Atleta, OutMixin):
    categoria: Annotated[CategoriaIn, Field(description='Categoria do atleta')]
    centro_treinamento: Annotated[CentroTreinamentoIn, Field(description='Centro de treinamento do atleta')]


# Schema para a atualização de um atleta (todos os campos são opcionais)
class AtletaUpdate(BaseSchema):
    nome: Annotated[Optional[str], Field(None, description='Nome do atleta', example='Joao', max_length=50)]
    idade: Annotated[Optional[int], Field(None, description='Idade do atleta', example=25)]


# Schema customizado para a listagem de atletas (endpoint GET /atletas)
class AtletaCustom(BaseSchema):
    nome: Annotated[str, Field(description='Nome do atleta', example='Joao', max_length=50)]
    categoria: Annotated[str, Field(description='Nome da categoria', example='Scale')]
    centro_treinamento: Annotated[str, Field(description='Nome do centro de treinamento', example='CT King')]
