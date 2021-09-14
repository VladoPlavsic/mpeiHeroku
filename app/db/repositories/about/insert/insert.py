from fastapi import HTTPException
from app.db.repositories.base import BaseDBRepository

from app.db.repositories.about.insert.queries import *

# create models
from app.models.about import CreateTeamMemberModel
from app.models.about import CreateAboutProjectModel
from app.models.about import CreateContactsModel

# response models
from app.models.about import TeamMemberInDBModel
from app.models.about import AboutProjectInDBModel
from app.models.about import ContactsInDBModel

import logging

logger = logging.getLogger(__name__)

class AboutDBInsertRepository(BaseDBRepository):
    """Insert data into about db schema."""
    async def insert_team_member(self, *, new_team: CreateTeamMemberModel) -> TeamMemberInDBModel:
        response = await self._fetch_one(query=insert_our_team_query(**new_team.dict()))
        return TeamMemberInDBModel(**response) if response else None

    async def insert_contacts(self, *, new_contacts: CreateContactsModel) -> ContactsInDBModel:
        response = await self._fetch_one(query=insert_contacts_query(**new_contacts.dict()))
        return ContactsInDBModel(**response) if response else None

    async def insert_about_project(self, *, new_about_project: CreateAboutProjectModel) -> AboutProjectInDBModel:
        response = await self._fetch_one(query=insert_about_project_query(**new_about_project.dict()))
        return AboutProjectInDBModel(**response) if response else None
