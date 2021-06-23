from typing import Optional
from pydantic import EmailStr

from fastapi import HTTPException

from databases import Database

from app.db.repositories.base import BaseDBRepository

from app.db.repositories.users.select.queries import *

from app.services import auth_service

# models
from app.models.user import UserInDB


import logging

logger = logging.getLogger(__name__)

class UsersDBSelectRepository(BaseDBRepository):
    
    def __init__(self, db: Database) -> None:
        super().__init__(db)
        self.auth_service = auth_service

    async def get_user_by_email(self, *, email: EmailStr) -> UserInDB:
        user_record = await self.__select_one(query=get_user_by_email_query(email=email))

        if not user_record:
            return None
        
        return UserInDB(**user_record)

    async def get_user_by_username(self, *, username: str) -> UserInDB:
        user_record = await self.__select_one(query=get_user_by_username_query(username=username))

        if not user_record:
            return None

        return UserInDB(**user_record)

    async def authenticate_user(self, *, email: EmailStr, password:str) -> Optional[UserInDB]:
        user = await self.get_user_by_email(email=email)
        if not user:
            return None
        if not self.auth_service.verify_password(password=password, salt=user.salt, hashed_password=user.password):
            return None
        
        return user

    async def check_code(self, *, user_id: int, code: str) -> bool:
        response = await self.__select_one(query=check_confirmation_code_query(user_id=user_id, confirmation_code=code))
        return response["valid"]

    async def set_confirmation_code(self, *, user_id: int, confirmation_code: str) -> str:
        response = await self.__select_one(query=set_confirmation_code_query(user_id=user_id, confirmation_code=confirmation_code))
        return response["code"]

    async def __select_one(self, *, query):
        try:
            record = await self.db.fetch_one(query=query)
        except Exception as e:
            logger.error("--- ERROR EXECUTING QUERY IN SELECT USERS REPOSITORY ---")
            logger.error(e)
            logger.error("--- ERROR EXECUTING QUERY IN SELECT USERS REPOSITORY ---")
            raise HTTPException(status_code=400, detail=f"Unhandled exception executing query in select users repository. Exited with {e}")
    
        return record


