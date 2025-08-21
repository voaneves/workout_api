from pydantic import BaseModel, EmailStr, Field
from workout_api.contrib.schemas import BaseSchema

class UserIn(BaseSchema):
    email: EmailStr = Field(..., description="Email do usuário")
    password: str = Field(..., min_length=6, max_length=60, description="Senha do usuário")

class UserOut(BaseSchema):
    id: int = Field(..., description="ID do usuário")
    email: EmailStr = Field(..., description="Email do usuário")

class TokenSchema(BaseModel):
    access_token: str
    token_type: str
