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
        """Function for updating news preview images presigned links."""
        keys = list(news.keys())
        links = list(news.values())
        await self._execute_one(query=update_news_links_query(keys=keys, links=links))

    async def update_images_links(self, *, images) -> None:
        """Function for updating news images presigned links."""
        keys = list(images.keys())
        links = list(images.values())
        await self._execute_one(query=update_news_images_links_query(keys=keys, links=links))

    async def update_news_metadata(self, *, updated: NewsUpdateModel) -> NewsInDBModel:
        response = await self._fetch_one(query=update_news_metadata_query(**updated.dict()))
        if not response:
            return None

        images = await self.select_news_images(fk=response['id'])
        return NewsInDBModel(**response, images=images)