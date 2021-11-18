from typing import List, Union

from app.db.repositories.base import BaseDBRepository

from app.models.user import UserUpdate
from app.models.user import PublicUserInDB

from app.db.repositories.users.update.queries import *


class UsersDBUpdateRepository(BaseDBRepository):
    
    async def update_user_information(self, *, id_: int, updated: UserUpdate) -> PublicUserInDB:
        """Updates user personal information based of id. Id should be retrived from JWT. Returns updated or NULL"""
        response = await self._fetch_one(query=update_user_information_query(id_=id_, **updated.dict()))
        return PublicUserInDB(**response) if response else None
        