from fastapi import HTTPException

from app.db.repositories.about.delete.queries import *

from app.db.repositories.base import BaseDBRepository

import logging

logger = logging.getLogger(__name__)

class AboutDBDeleteRepository(BaseDBRepository):
    """Allows deleting from db schema about."""
    async def delete_team_member(self, *, id: int) -> None:
        response = await self._fetch_one(query=delete_team_member_query(id=id))
        return response['deleted'] if response else None

    async def delete_about_project(self, *, id: int) -> None:
        await self._execute_one(query=delete_about_project_query(id=id))

    async def delete_contact(self, *, id: int) -> None:
        await self._execute_one(query=delete_contact_query(id=id))
