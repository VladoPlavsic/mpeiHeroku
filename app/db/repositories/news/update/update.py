from typing import Optional
from fastapi import HTTPException

from app.db.repositories.news.update.queries import *

from app.db.repositories.base import BaseDBRepository

from app.models.news import NewsUpdateModel
from app.models.news import NewsInDBModel

import logging

logger = logging.getLogger(__name__)

class NewsDBUpdateRepository(BaseDBRepository):

    async def update_news_links(self, *, news) -> None:
        """
        Accepts dict with keys = 'image key' and value = 'sharing link'
        Updates table news.news_images by keys
        """
        keys = list(news.keys())
        links = list(news.values())

        await self.__update(query=update_news_links_query(keys=keys, links=links))

    async def update_images_links(self, *, images) -> None:
        """
        Accepts dict with keys = 'image key' and value = 'sharing link'
        Updates table news.news_images by keys
        """
        keys = list(images.keys())
        links = list(images.values())
        await self.__update(query=update_news_images_links_query(keys=keys, links=links))

    async def update_news_metadata(self, *, updated: NewsUpdateModel) -> NewsInDBModel:
        
        response = await self.__update(query=update_news_metadata_query(
            id=updated.id, 
            date=updated.date, 
            title=updated.title, 
            short_desc=updated.short_desc, 
            content=updated.content, 
            url=updated.url, 
            cloud_key=updated.cloud_key, 
            preview_image_url=updated.preview_image_url))

        images = await self.select_news_images(fk=response['id'])

        return NewsInDBModel(**response, images=images) if response else None

    async def __update(self, *, query):
        try:
            response = await self.db.fetch_one(query=query)
        except Exception as e:
            logger.error("--- ERROR UPDATING NEWS ---")                
            logger.error(e)
            logger.error("--- ERROR UPDATING NEWS ---")                
            raise HTTPException(status_code=400, detail=f"Unhandled error. Exiter with {e}")

        return response