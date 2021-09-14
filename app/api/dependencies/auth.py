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
    """Takes in JWT token. Returns UserInDB or raises 401 if token expired or not valid"""
    try:
        user = auth_service.get_user_from_token(token=token, secret_key=str(SECRET_KEY))
    except Exception as e:
        raise e

    if not user:
        raise HTTPException(status_code=404, detail="No user found!")

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

    if not user.email_verified:
        raise HTTPException(status_code=401, detail="Email not verified!")

    return user.email_verified

async def allowed_or_denied(
    is_superuser = Depends(is_superuser),
    is_verified = Depends(is_verified),
    ) -> bool:
    """If user is not superuser, or his email is not verified raise Exception, otherwise return True"""
    if not is_superuser:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not superuser!")
    
    return True

def generate_confirmation_code() -> str:
    from random import randint
    return str(randint(100000, 999999))
