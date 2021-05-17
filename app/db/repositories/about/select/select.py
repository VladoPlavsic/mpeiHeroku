from typing import List
from fastapi import HTTPException

from app.db.repositories.about.select.query import *

from app.db.repositories.base import BaseDBRepository

from app.models.about import TeamMemberInDBModel
from app.models.about import AboutProjectInDBModel
from app.models.about import ContactsInDBModel


import logging

logger = logging.getLogger(__name__)

class AboutDBSelectRepository(BaseDBRepository):


    async def select_all_team_members(self) -> List[TeamMemberInDBModel]:
        response = await self.__select_many(query=select_all_team_members_query())
        return [TeamMemberInDBModel(**r) for r in response]

    async def select_all_about_project(self) -> List[AboutProjectInDBModel]:
        response = await self.__select_many(query=select_all_about_project_query())
        return [AboutProjectInDBModel(**r) for r in response]

    async def select_all_contacts(self) -> List[ContactsInDBModel]:
        response = await self.__select_many(query=select_all_contacts_query())
        return [ContactsInDBModel(**r) for r in response]

    async def __select_one(self, *, query):
        pass

    async def __select_many(self, *, query): 
        try:
            response = await self.db.fetch_all(query=query)
        except Exception as e:
            logger.error("--- ERROR FETCHING MANY ABOUT ---")
            logger.error(e)
            logger.error("--- ERROR FETCHING MANY ABOUT ---")
            raise HTTPException(status_code=400, detail=f"Unhandled error fetching many from about. Exited with {e}")

        return response
