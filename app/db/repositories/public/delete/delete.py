from fastapi import HTTPException

from app.db.repositories.base import BaseDBRepository

from app.db.repositories.public.delete.queries import *


import logging

logger = logging.getLogger(__name__)

class PublicDBDeleteRepository(BaseDBRepository):

    async def delete_video(self) -> str:
        """Deletes video. Video does not have to have object_key!"""
        response = await self._fetch_one(query=delete_video_query())
        return response['object_key'] if response else None

    async def delete_intro_video(self) -> str:
        """Deletes intro video. Intro video does not have to have object_key!"""
        response = await self._fetch_one(query=delete_intro_video_query())
        return response['object_key'] if response else None

    async def delete_quiz(self) -> str:
        """Deletes quiz entirely and returns list of deleted object_keys."""
        records = await self._fetch_many(query=delete_quiz_query())
        return [record['object_key'] for record in records if record['object_key']]

    async def delete_quiz_question(self, *, id) -> str:
        """Deletes quiz. Quiz does not have to have object_key!"""
        response = await self._fetch_one(query=delete_quiz_question_query(id=id))
        return response['object_key'] if response else None

    async def delete_game(self) -> bool:
        return await self.__delete(query=delete_game_query())

    async def delete_book(self) -> str:
        return await self.__delete(query=delete_book_query())

    async def delete_theory(self) -> str:
        return await self.__delete(query=delete_theory_query())

    async def delete_practice(self) -> str:
        return await self.__delete(query=delete_practice_query())

    async def delete_about_us(self, *, order_number) -> bool:
        await self._execute_one(query=delete_about_us_query(order_number=order_number))

    async def delete_faq(self, *, id) -> bool:
        await self._execute_one(query=delete_faq_query(id=id))

    async def delete_instruction(self, *, order_number) -> bool:
        await self._execute_one(query=delete_instruction_query(order_number=order_number))

    async def delete_review(self, *, id) -> bool:
        await self._execute_one(query=delete_review_query(id=id))

    async def __delete(self, *, query) -> bool:
        """Executes query and tries to return deleted key or raise HTTPException"""
        response = await self._fetch_one(query=query)
        if not response['object_key']:
            raise HTTPException(status_code=404, detail="Trying to delete returned nothing.")
        return response['object_key']