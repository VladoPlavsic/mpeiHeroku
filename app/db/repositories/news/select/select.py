from typing import List
from fastapi import HTTPException

from app.db.repositories.base import BaseDBRepository

from app.db.repositories.news.select.queries import *

from app.models.news import NewsAllModel
from app.models.news import NewsImagesAllModel
from app.models.news import NewsImagesInDB
from app.models.news import NewsInDBModel
from app.models.news import NewsPreviewInDBModel

import logging

logger = logging.getLogger(__name__)

class NewsDBSelectRepository(BaseDBRepository):

    async def select_news_images(self, *, fk: int) -> List[NewsImagesInDB]:
        """Returns list of images (NewsImagesInDB) based on news foreign key they belong to."""
        records = await self._fetch_many(query=select_images_for_news_query(fk=fk))
        return [NewsImagesInDB(**record) for record in records]

    async def select_all_news(self) -> List[NewsAllModel]:
        """Returns list of object_keys for all news preview images in database"""
        records = await self._fetch_many(query=select_all_news_query())
        return [NewsAllModel(**record) for record in records]

    async def select_all_news_images(self) -> List[NewsImagesAllModel]:
        """Returns list of object_keys for all news images in database"""
        records = await self._fetch_many(query=select_all_news_images_query())
        return [NewsImagesAllModel(**record) for record in records] 

    async def select_news_preview(self, *, start: int, count: int) -> List[NewsPreviewInDBModel]:
        """Returns list of preview images (NewsPreviewInDBModel) from db.
        
        Keyword arguments:
        start -- starting offset for images 
        count -- number of images to fetch
            (e.g. If there is 15 images, and we want 12-14 we would set these parameters to be:
                start = 11
                count = 3)
        """
        records = await self._fetch_many(query=select_news_preview_query(start=start, count=count))
        return [NewsPreviewInDBModel(**record) for record in records]

    async def select_news(self, *, date: str, url: str) -> NewsInDBModel:
        news = await self._fetch_one(query=select_news_query(date=date, url=url))
        if not news:
            raise HTTPException(status_code=404, detail=f"News not found!")

        images = await self.select_news_images(fk=news['id'])
        return NewsInDBModel(**news, images=images)

    async def get_news_count(self) -> int:
        response = await self._fetch_one(query=get_news_count_query())
        return response['count']
