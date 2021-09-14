from fastapi import HTTPException

from app.db.repositories.about.update.queries import *

from app.db.repositories.base import BaseDBRepository

# update models
from app.models.about import UpdateTeamMemberModel
from app.models.about import UpdateContactsModel
from app.models.about import UpdateAboutProjectModel

# response models
from app.models.about import TeamMemberInDBModel
from app.models.about import ContactsInDBModel
from app.models.about import AboutProjectInDBModel

import logging

logger = logging.getLogger(__name__)

class AboutDBUpdateRepository(BaseDBRepository):
    """Allows updating data in db schema about."""
    async def update_team_member_photos(self, *, photos) -> None:
        """Function used in CRON job for updating presigned links every 6 days"""
        keys = list(photos.keys())
        links = list(photos.values())
        await self._execute_one(query=update_team_member_photos_query(object_keys=keys, photo_links=links))

    async def update_team_member(self, *, updated: UpdateTeamMemberModel) -> TeamMemberInDBModel:
        response = await self._fetch_one(query=update_team_member_query(**updated.dict()))
        return TeamMemberInDBModel(**response) if response else None
    
    async def update_contact(self, *, updated: UpdateContactsModel) -> ContactsInDBModel:
        response = await self._fetch_one(query=update_contact_query(**updated.dict()))
        return ContactsInDBModel(**response) if response else None

    async def update_about_project(self, *, updated: UpdateAboutProjectModel) -> AboutProjectInDBModel:
        response = await self._fetch_one(query=update_about_project_query(**updated.dict()))
        return AboutProjectInDBModel(**response) if response else None
