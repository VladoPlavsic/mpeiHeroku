from fastapi import HTTPException

from app.db.repositories.base import BaseDBRepository

from app.db.repositories.news.delete.queires import *

import logging

logger = logging.getLogger(__name__)

class NewsDBDeleteRepository(BaseDBRepository):
    async def delete_news(self, *, id: int) -> None:
        response = await self._fetch_one(query=delete_news_query(id=id))
        return response['object_key'] if response else None
