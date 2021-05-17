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

    async def update_team_member_photos(self, *, photos) -> None:
        keys = list(photos.keys())
        links = list(photos.values())
        await self.__update(query=update_team_member_photos_query(photo_keys=keys, photo_links=links))

    async def update_team_member(self, *, updated: UpdateTeamMemberModel) -> TeamMemberInDBModel:
        response = await self.__update(query=update_team_member_query(**updated.dict()))
        if not response:
            raise HTTPException(status_code=404, detail="Oops! No team members updated!")
        return TeamMemberInDBModel(**response)
    
    async def update_contact(self, *, updated: UpdateContactsModel) -> ContactsInDBModel:
        response = await self.__update(query=update_contact_query(**updated.dict()))
        if not response:
            raise HTTPException(status_code=404, detail="Oops! No contacts updated!")
        return ContactsInDBModel(**response)

    async def update_about_project(self, *, updated: UpdateAboutProjectModel) -> AboutProjectInDBModel:
        response = await self.__update(query=update_about_project_query(**updated.dict()))
        if not response:
            raise HTTPException(status_code=404, detail="Oops! No about project updated!")
        return AboutProjectInDBModel(**response)


    async def __update(self, *, query):
        try:
            response = await self.db.fetch_one(query=query)
        except Exception as e:
            logger.error("--- ERROR UPDATING ABOUT ---")
            logger.error(e)
            logger.error("--- ERROR UPDATING ABOUT ---")
            raise HTTPException(status_code=400, detail=f"Unhandled error trying to update about. Exited with {e}")
     
        return response