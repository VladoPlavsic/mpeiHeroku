from typing import List
from fastapi import HTTPException

from app.db.repositories.base import BaseDBRepository

from app.db.repositories.news.select.queries import *

from app.models.news import NewsAllModel
from app.models.news import NewsImagesAllModel
from app.models.news import NewsImagesInDB
from app.models.news import NewsInDBModel

import logging

logger = logging.getLogger(__name__)

class NewsDBSelectRepository(BaseDBRepository):

    async def select_all_news(self) -> List[NewsAllModel]:
        """
        Returns list of keys for all news preview images in database
        """
        records = await self.__select_many(query=select_all_news_query())

        response = [NewsAllModel(**record) for record in records]
        return response

    async def select_all_news_images(self) -> List[NewsImagesAllModel]:
        """
        Returns list of keys for all news images in database
        """
        records = await self.__select_many(query=select_all_news_images_query())

        response = [NewsImagesAllModel(**record) for record in records] 
        return response


    async def select_news_images(self, *, fk: int) -> List[NewsImagesInDB]:
        images_records = await self.__select_many(query=select_images_for_news_query(fk=fk))
        return [NewsImagesInDB(**image) for image in images_records]

    async def select_news(self, *, start: int, count: int) -> List[NewsInDBModel]:
        news_records = await self.__select_many(query=select_news_query(start=start, count=count))
        response = [NewsInDBModel(**news, images=[]) for news in news_records]

        for news in response:
            news.images = await self.select_news_images(fk=news.id)

        print(response)

        return response

    async def get_news_count(self) -> int:
        response = await self.__select_one(query=get_news_count_query())

        return response['count']

    async def __select_one(self, *, query):
        try:
            response = await self.db.fetch_one(query=query)
        except Exception as e:
            logger.error("--- ERROR SELECTING NEWS ---")                
            logger.error(e)
            logger.error("--- ERROR SELECTING NEWS ---")                
            raise HTTPException(status_code=400, detail=f"Unhandled error. Exiter with {e}")

        return response

    async def __select_many(self, *, query):
        try:
            response = await self.db.fetch_all(query=query)
        except Exception as e:
            logger.error("--- ERROR SELECTING NEWS ---")                
            logger.error(e)
            logger.error("--- ERROR SELECTING NEWS ---")                
            raise HTTPException(status_code=400, detail=f"Unhandled error. Exiter with {e}")

        return response