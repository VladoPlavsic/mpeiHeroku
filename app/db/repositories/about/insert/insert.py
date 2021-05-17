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
    
    async def insert_our_team(self, *, new_team: CreateTeamMemberModel) -> TeamMemberInDBModel:
        response = await self.__insert(query=insert_our_team_query(**new_team.dict()))
        if not response:
            raise HTTPException(status_code=400, detail="Ooops! Something went wrong. Team member not added")
        return TeamMemberInDBModel(**response)

    async def insert_contacts(self, *, new_contacts: CreateContactsModel) -> ContactsInDBModel:
        response = await self.__insert(query=insert_contacts_query(**new_contacts.dict()))
        if not response:
            raise HTTPException(status_code=400, detail="Ooops! Something went wrong. Contacts not added")
        return ContactsInDBModel(**response)

    async def insert_about_project(self, *, new_about_project: CreateAboutProjectModel) -> AboutProjectInDBModel:
        response = await self.__insert(query=insert_about_project_query(**new_about_project.dict()))
        if not response:
            raise HTTPException(status_code=400, detail="Ooops! Something went wrong. About project not added")
        return AboutProjectInDBModel(**response)

    async def __insert(self, *, query):
        try:
            response = await self.db.fetch_one(query=query)
        except Exception as e:
            logger.error("--- ERROR INSERTING ABOUT ---")
            logger.error(e)
            logger.error("--- ERROR INSERTING ABOUT ---")
            raise HTTPException(status_code=400, detail=f"Unhandled error raised trying to insert about. Exited with {e}")
        
        return response