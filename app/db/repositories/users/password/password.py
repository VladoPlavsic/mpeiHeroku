from app.db.repositories.base import BaseDBRepository
from fastapi import HTTPException

from app.db.repositories.users.password.queries import *

import logging

logger = logging.getLogger(__name__)


class UsersDBPasswordRepository(BaseDBRepository):
    # create reset password request
    async def request_reset_password(self, *, email: str) -> str:
        response = await self.__execute(query=reset_password_request_query(email=email))
        return response["recovery_key"] if response else None 

    # confirm password reset request and return secret key for reseting
    async def confirm_reset_password(self, *, email: str, recovery_key: str) -> str:
        response = await self.__execute(query=confirm_password_recovery_query(email=email, recovery_key=recovery_key))
        return response["recovery_hash"] if response else None

    # reset password
    async def reset_password(self, *, recovery_hash: str, password: str) -> bool:
        salt_and_password = self.auth_service.create_salt_and_hash_password(plaintext_password=password)
        response = await self.__execute(query=recover_password_query(hash_=recovery_hash, password=salt_and_password.password, salt=salt_and_password.salt))
        return response["updated"]

    async def __execute(self, *, query): 
        try:
            response = await self.db.fetch_one(query=query)
        except Exception as e:
            logger.error("ERROR IN USER PASSWORD REPOSITORY")
            logger.error(e)
            logger.error("ERROR IN USER PASSWORD REPOSITORY")            
            raise HTTPException(status_code=400, detail=f"Unhandled exception raised in user password repository. Exited with {e}")

        return response







