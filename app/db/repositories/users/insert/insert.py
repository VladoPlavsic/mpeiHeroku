from fastapi import HTTPException

from app.db.repositories.base import BaseDBRepository

from app.db.repositories.users.insert.queries import *

from app.models.user import UserCreate
from app.models.user import UserInDB, UserInDB

import logging

logger = logging.getLogger(__name__)

class UserDBInsertRepository(BaseDBRepository):

    async def register_new_user(self, new_user: UserCreate) -> UserInDB:
        # make sure email is not taken
        if await self.get_user_by_email(email=new_user.email):
            raise HTTPException(
                status_code=409,
                detail="This email is already taken. Login whith that email or register with new one!"
            )
        
        user_password_update = self.auth_service.create_salt_and_hash_password(plaintext_password=new_user.password)
        new_user_params = new_user.copy(update=user_password_update.dict())
        registred = await self.__execute(query=register_new_user_query(**new_user_params.dict()))

        return UserInDB(**registred)

    async def set_jwt_token(self, *, user_id: int, token: str):
        await self.__execute(query=set_jwt_token_query(user_id=user_id, token=token))

    async def verify_email(self, *, user_id: int):
        await self.__execute(query=verify_email_query(user_id=user_id))


    async def add_grade_to_user(self, *, user_id: int, grade_id: int, days: int, for_life: bool = False):
        await self.__execute(query=add_grade_to_user_query(user_id=user_id, grade_id=grade_id, days=days, for_life=for_life))

    async def add_subject_to_user(self, *, user_id: int, subject_id: int, days: int, for_life: bool = False):
        await self.__execute(query=add_subject_to_user_query(user_id=user_id, subject_id=subject_id, days=days, for_life=for_life))

    async def __execute(self, *, query): 
        try:
            response = await self.db.fetch_one(query=query)
        except Exception as e:
            logger.error("ERROR IN USER INSERT REPOSITORY")
            logger.error(e)
            logger.error("ERROR IN USER INSERT REPOSITORY")            
            raise HTTPException(status_code=400, detail=f"Unhandled exception raised in user insert repository. Exited with {e}")

        return response
