from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from workout_api.auth.models import UserModel
from workout_api.auth.schemas import TokenSchema, UserIn, UserOut
from workout_api.auth.security import create_access_token, get_password_hash, verify_password
from workout_api.auth.dependencies import get_current_user
from workout_api.contrib.dependencies import DatabaseDependency

router = APIRouter(tags=["auth"])

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def register(db_session: DatabaseDependency, user_in: UserIn = Body(...)):
    try:
        hashed_password = get_password_hash(user_in.password)
        user = UserModel(email=user_in.email, hashed_password=hashed_password)
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        return user
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

@router.post("/token", response_model=TokenSchema)
async def login_for_access_token(db_session: DatabaseDependency, form_data: OAuth2PasswordRequestForm = Depends()):
    user = (await db_session.execute(select(UserModel).filter_by(email=form_data.username))).scalars().first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
async def read_users_me(current_user: UserModel = Depends(get_current_user)):
    return current_user
