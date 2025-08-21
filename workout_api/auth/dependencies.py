from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.future import select
from workout_api.auth.models import UserModel
from workout_api.auth.security import decode_access_token
from workout_api.contrib.dependencies import DatabaseDependency

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

async def get_current_user(token: str = Depends(oauth2_scheme), db_session: DatabaseDependency = Depends()):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception
        
    user = (await db_session.execute(select(UserModel).filter_by(email=email))).scalars().first()
    if user is None:
        raise credentials_exception
        
    return user
