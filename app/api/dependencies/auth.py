from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.config import SECRET_KEY, API_PREFIX
from app.models.user import UserInDB
from app.api.dependencies.database import get_db_repository
from app.db.repositories.users.users import UsersDBRepository
from app.services import auth_service

import logging

logger = logging.getLogger(__name__)

async def get_user_from_token(
    *,
    token: str,
    user_repo: UsersDBRepository = Depends(get_db_repository(UsersDBRepository)),
    ) -> Optional[UserInDB]:
    '''
        Takes in JWT token 
        Returns UserInDB or raises 401 if: token expired, not valid token
    '''
    try:
        email = auth_service.get_user_from_token(token=token, secret_key=str(SECRET_KEY))
        user = await user_repo.get_user_by_email(email=email)
    except Exception as e:
        raise e

    if not user:
        raise HTTPException(status_code=404, detail="No user found!")

    if user.jwt != token:
        raise HTTPException(status_code=401, detail="Session expired.")

    return user

async def is_superuser(
    *,
    user: UserInDB = Depends(get_user_from_token),
    ) -> bool:

    return user.is_superuser

async def is_verified(
    *,
    user: UserInDB = Depends(get_user_from_token),
    ) -> bool:

    return user.email_verified

async def get_current_active_user(current_user: UserInDB = Depends(get_user_from_token)) -> Optional[UserInDB]:
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No authenticated user.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not an active user.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return current_user


def generate_confirmation_code() -> str:
    from random import randint
    return str(randint(100000, 999999))
