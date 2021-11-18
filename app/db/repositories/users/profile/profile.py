from typing import List
from app.db.repositories.base import BaseDBRepository
from app.db.repositories.users.profile.queries import *
from app.models.user import UserDeletion

class UsersDBProfileRepository(BaseDBRepository):
  
    async def deactivate_profile(self, *, user_id: int) -> None:
        """Deactivates profile based on user_id"""
        await self._execute_one(query=deactivate_profile_query(user_id=user_id))

    async def delete_profile(self, *, user_id: int) -> None:
        """Deletes profile based on user_id"""
        await self._execute_one(query=delete_profile_query(user_id=user_id))

    async def select_deactivated_profiles_for_warning_month(self) -> List[UserDeletion]:
        """Retrive all profiles that will be deleted in a month"""
        response = await self._fetch_many(query=select_deactivated_profiles_for_warning_month_query())
        return [UserDeletion(**user) for user in response]

    async def select_deactivated_profiles_for_warning_week(self) -> List[UserDeletion]:
        """Retrive all profiles that will be deleted in a week"""
        response = await self._fetch_many(query=select_deactivated_profiles_for_warning_week_query())
        return [UserDeletion(**user) for user in response]

    async def select_deactivated_profiles_for_deletion(self) -> List[UserDeletion]:
        """Retrive all profiles that have been deactivated more then 3 months ago"""
        response = await self._fetch_many(query=select_deactivated_profiles_for_deletion_query())
        return [UserDeletion(**user) for user in response]

    async def create_confirmation_hash_for_reactivation(self, *, user_id: int) -> str:
        """Creates reactivation hash for profile reactivation and returns it, or NULL if no user found by given user_id"""
        response = await self._fetch_one(query=create_reactivation_request_query(user_id=user_id))
        return response["reactivation_hash"] if response["reactivation_hash"] else None

    async def activate_profile(self, *, reactivation_hash: str) -> bool:
        """Try reactivating profile based on hash and id. If successful return True else False"""
        response = await self._fetch_one(query=activate_profile_query(reactivation_hash=reactivation_hash))
        return response["activated"]
