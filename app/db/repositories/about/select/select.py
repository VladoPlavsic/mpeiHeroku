from typing import List
from fastapi import HTTPException

from app.db.repositories.about.select.queries import *

from app.db.repositories.base import BaseDBRepository

from app.models.about import TeamMemberInDBModel
from app.models.about import AboutProjectInDBModel
from app.models.about import ContactsInDBModel

import logging

logger = logging.getLogger(__name__)

class AboutDBSelectRepository(BaseDBRepository):
    """Fetch data from about schema."""
    async def select_all_team_members(self) -> List[TeamMemberInDBModel]:
        records = await self._fetch_many(query=select_all_team_members_query())
        return [TeamMemberInDBModel(**record) for record in records]

    async def select_all_about_project(self) -> List[AboutProjectInDBModel]:
        records = await self._fetch_many(query=select_all_about_project_query())
        return [AboutProjectInDBModel(**record) for record in records]

    async def select_all_contacts(self) -> List[ContactsInDBModel]:
        records = await self._fetch_many(query=select_all_contacts_query())
        return [ContactsInDBModel(**record) for record in records]
