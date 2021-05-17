from typing import List
from fastapi import HTTPException

from app.db.repositories.news.insert.queries import *

from app.db.repositories.base import BaseDBRepository

# create models
from app.models.news import NewsCreateModel
from app.models.news import NewsImagesCreate

# response models
from app.models.news import NewsInDBModel
from app.models.news import NewsImagesCore

import logging

logger = logging.getLogger(__name__)

class NewsDBInsertRepository(BaseDBRepository):

    async def insert_news(self, *, news: NewsCreateModel) -> NewsInDBModel:
        metadata = await self.__execute_one(query=insert_news_master_query(
            cloud_key=news.cloud_key,
            content=news.content,
            date=news.date,
            preview_image_url=news.preview_image_url,
            short_desc=news.short_desc,
            title=news.title,
            url=news.url))
        images = await self.__insert_news_slave(fk=metadata['id'], images=news.images)

        return NewsInDBModel(**metadata, images=images)

    async def __insert_news_slave(self, *, fk: int, images: List[NewsImagesCreate]) -> NewsImagesCore:
        records = await self.__execute_many(query=insert_news_slave_query(fk=fk, medium=images))
        return [NewsImagesCore(**r) for r in records]

    async def __execute_one(self, *, query):
        try:
            response = await self.db.fetch_one(query=query)
        except Exception as e:
            logger.error("--- ERROR EXECUTING NEWS INSERT QUERY ---")
            logger.error(e)
            logger.error("--- ERROR EXECUTING NEWS INSERT QUERY ---")
            raise HTTPException(status_code=400, detail=f"Unhandled error raised. Exited with {e}")

        return response


    async def __execute_many(self, *, query):
        try:
            response = await self.db.fetch_all(query=query)
        except Exception as e:
            logger.error("--- ERROR EXECUTING NEWS INSERT QUERY ---")
            logger.error(e)
            logger.error("--- ERROR EXECUTING NEWS INSERT QUERY ---")
            raise HTTPException(status_code=400, detail=f"Unhandled error raised. Exited with {e}")

        return response
