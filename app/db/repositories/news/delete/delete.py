from fastapi import HTTPException

from app.db.repositories.base import BaseDBRepository

from app.db.repositories.news.delete.queires import *

import logging

logger = logging.getLogger(__name__)

class NewsDBDeleteRepository(BaseDBRepository):

    async def delete_news(self, *, id: int) -> None:
        response = await self.__execute(query=delete_news_query(id=id))
        return response['cloud_key']

    async def __execute(self, *, query):
        try:
            response = await self.db.fetch_one(query=query)
        except Exception as e:
            logger.error("--- ERROR DELETING NEWS ---")                
            logger.error(e)
            logger.error("--- ERROR DELETING NEWS ---")                
            raise HTTPException(status_code=400, detail=f"Unhandled error. Exiter with {e}")

        return response
