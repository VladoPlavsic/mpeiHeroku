from app.db.repositories.base import BaseDBRepository
from app.db.repositories.users.password.queries import *

class UsersDBPasswordRepository(BaseDBRepository):
    async def request_reset_password(self, *, email: str) -> str:
        """Creates new password reset request and stores in database.
        
        Returns:
        recovery_key - sha256 encrypted key that belongs to a given user
        """
        response = await self._fetch_one(query=reset_password_request_query(email=email))
        return response["recovery_key"] if response else None 

    async def confirm_reset_password(self, *, recovery_key: str) -> str:
        """Confirms password reset request.
        
        Creates new recovery_hash secret key and returns it.
        If the recovery_key wasn't verified, returns None.
        """
        response = await self._fetch_one(query=confirm_password_recovery_query(recovery_key=recovery_key))
        return response["recovery_hash"] if response else None

    async def reset_password(self, *, recovery_hash: str, password: str) -> bool:
        """Creates hashed_password and salt with new values based on user provided plain text password.

        Updates password and hash if recovery_hash is valid.
        If not returns false.
        """
        salt_and_password = self.auth_service.create_salt_and_hash_password(plaintext_password=password)
        response = await self._fetch_one(query=recover_password_query(hash_=recovery_hash, password=salt_and_password.password, salt=salt_and_password.salt))
        return response["updated"]
