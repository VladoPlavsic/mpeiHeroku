from fastapi import HTTPException

from app.db.repositories.base import BaseDBRepository

from app.db.repositories.public.delete.queries import *


import logging

logger = logging.getLogger(__name__)

class PublicDBDeleteRepository(BaseDBRepository):

    async def delete_video(self) -> bool:
        return await self.__delete(query=delete_video_query())

    async def delete_game(self) -> bool:
        return await self.__delete(query=delete_game_query())

    async def delete_book(self) -> str:
        '''
        Deletes book from book table and returns NOTE: book key! (not folder but book itself)
        or false if nothing was deleted
        '''
        return await self.__delete(query=delete_book_query(), getResponse=True)

    async def delete_theory(self) -> str:
        '''
        Deletes theory from table and returns theory folder key
        or false if nothing was deleted
        '''
        return await self.__delete(query=delete_theory_query(), getResponse=True)

    async def delete_practice(self) -> str:
        '''
        Deletes practice from table and returns practice folder key
        or false if nothing was deleted
        '''
        return await self.__delete(query=delete_practice_query(), getResponse=True)

    async def delete_about_us(self, *, order_number) -> bool:
        return await self.__delete(query=delete_about_us_query(order_number=order_number))

    async def delete_faq(self, *, id) -> bool:
        return await self.__delete(query=delete_faq_query(id=id))

    async def delete_instruction(self, *, order_number) -> bool:
        return await self.__delete(query=delete_instruction_query(order_number=order_number))

    async def __delete(self, *, query, getResponse=False) -> bool:
        try:
            response = await self.db.fetch_one(query=query)
        except Exception as e:
            logger.error("--- ERROR DELETING FROM PUBLIC ---")
            logger.error(e)
            logger.error("--- ERROR DELETING FROM PUBLIC ---")
            raise HTTPException(status_code=400, detail=f"Error raised trying to delete. Exited with {e}")

        if getResponse:
            return response['key']
        
        return False