from typing import Optional
from pydantic import EmailStr

from databases import Database

from app.db.repositories.base import BaseDBRepository

from app.db.repositories.users.select.queries import *

from app.services import auth_service

from app.models.user import UserInDB

class UsersDBSelectRepository(BaseDBRepository):
    def __init__(self, db: Database) -> None:
        super().__init__(db)
        self.auth_service = auth_service

    async def get_user_by_email(self, *, email: EmailStr) -> UserInDB:
        user_record = await self._fetch_one(query=get_user_by_email_query(email=email))
        return UserInDB(**user_record) if user_record else None

    async def get_user_by_username(self, *, username: str) -> UserInDB:
        user_record = await self._fetch_one(query=get_user_by_username_query(username=username))
        return UserInDB(**user_record) if user_record else None


    async def authenticate_user(self, *, email: EmailStr, password:str) -> Optional[UserInDB]:
        user = await self.get_user_by_email(email=email)
        if user:
            if self.auth_service.verify_password(password=password, salt=user.salt, hashed_password=user.password):
                return user
        
        return None

    async def check_refresh_token(self, *, user: UserInDB, refresh_token: str) -> Optional[UserInDB]:
        user = await self.get_user_by_email(email=user.email)
        if user:
            if user.jwt != refresh_token:
                return user
        
        return None

    async def check_code(self, *, user_id: int, code: str) -> bool:
        response = await self._fetch_one(query=check_confirmation_code_query(user_id=user_id, confirmation_code=code))
        return response["valid"]
