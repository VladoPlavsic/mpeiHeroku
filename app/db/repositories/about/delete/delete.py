from fastapi import HTTPException

from app.db.repositories.about.delete.queries import *

from app.db.repositories.base import BaseDBRepository

import logging

logger = logging.getLogger(__name__)

class AboutDBDeleteRepository(BaseDBRepository):

    async def delete_team_member(self, *, id: int) -> None:
        await self.__delete(query=delete_team_member_query(id=id))

    async def delete_about_project(self, *, id: int) -> None:
        await self.__delete(query=delete_about_project_query(id=id))

    async def delete_contact(self, *, id: int) -> None:
        await self.__delete(query=delete_contact_query(id=id))

    async def __delete(self, *, query):
        try:
            response = await self.db.fetch_one(query=query)
        except Exception as e:
            logger.error("--- ERROR DELETING ABOUT ---")
            logger.error(e)
            logger.error("--- ERROR DELETING ABOUT ---")
            raise HTTPException(status_code=400, detail=f"Unhandled error deleting from about. Exited with {e}")
        
        return response