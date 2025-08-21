from typing import Annotated
from pydantic import BaseModel, ConfigDict, UUID4, Field
from datetime import datetime


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        extra='forbid',         # Não permite campos extras nos modelos
        from_attributes=True    # Permite a conversão de modelos SQLAlchemy para Pydantic
    )


class OutMixin(BaseSchema):
    id: Annotated[UUID4, Field(description='Identificador')]
    created_at: Annotated[datetime, Field(description='Data de criação')]
