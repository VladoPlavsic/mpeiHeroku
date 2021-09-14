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

    async def insert_news_check(self, *, date, url) -> bool:
        """Check if news can be inserted"""
        response = await self._fetch_one(query=insert_news_check_query(date=date, url=url))
        return response['yes']

    async def insert_news(self, *, news: NewsCreateModel) -> NewsInDBModel:
        metadata = await self._fetch_one(query=insert_news_master_query(
            date=news.date,
            title=news.title, 
            short_desc=news.short_desc,
            content=news.content,
            url=news.url,
            object_key=news.object_key,
            preview_image_url=news.preview_image_url
        ))
        if not metadata:
            return None

        images = await self.__insert_news_slave(fk=metadata['id'], images=news.images)
        return NewsInDBModel(**metadata, images=images)

    async def __insert_news_slave(self, *, fk: int, images: List[NewsImagesCreate]) -> NewsImagesCore:
        records = await self._fetch_many(query=insert_news_slave_query(fk=fk, medium=images))
        return [NewsImagesCore(**record) for record in records]
