from typing import Union
from fastapi import HTTPException

from app.db.repositories.public.update.queries import *

from app.db.repositories.base import BaseDBRepository

# update models
from app.models.public import UpdateVideoModel
from app.models.public import UpdateGameModel
from app.models.public import UpdateAboutUsModel
from app.models.public import UpdateFAQModel
from app.models.public import UpdateInstructionModel

# response models
from app.models.public import VideoInDB
from app.models.public import GameInDB
from app.models.public import AboutUsInDB
from app.models.public import FAQInDB
from app.models.public import InstructionInDB

import logging

logger = logging.getLogger(__name__)

class PublicDBUpdateRepository(BaseDBRepository):

    async def update_video(self, *, updated: UpdateVideoModel) -> VideoInDB:
        response = await self.__update(query=update_video_query(name_ru=updated.name_ru, url=updated.url, description=updated.description))
        if not response:
            raise HTTPException(status_code=404, detail="Ooops! Didn't find anything to update in table video")

        return VideoInDB(**response)

    async def update_game(self, *, updated: UpdateGameModel) -> GameInDB:
        response = await self.__update(query=update_game_query(name_ru=updated.name_ru, url=updated.url, description=updated.description))
        if not response:
            raise HTTPException(status_code=404, detail="Ooops! Didn't find anything to update in table game")

        return GameInDB(**response)

    async def update_about_us(self, *, updated: UpdateAboutUsModel) -> AboutUsInDB:
        response = await self.__update(query=update_about_us_query(order_number=updated.order, title=updated.title, description=updated.description, svg=updated.svg))
        if not response:
            raise HTTPException(status_code=404, detail="Ooops! Didn't find anything to update in table about us")

        return AboutUsInDB(**response)

    async def update_faq(self, *, updated: UpdateFAQModel) -> FAQInDB:
        response = await self.__update(query=update_faq_query(id=updated.id, question=updated.question, answer=updated.answer))
        if not response:
            raise HTTPException(status_code=404, detail="Ooops! Didn't find anything to update in table FAQ")

        return FAQInDB(**response)


    async def update_instruction(self, *, updated: UpdateInstructionModel) -> InstructionInDB:
        response = await self.__update(query=update_instruction_query(order_number=updated.order, title=updated.title, description=updated.description))
        if not response:
            raise HTTPException(status_code=404, detail="Ooops! Didn't find anything to update in table Instruction")

        return InstructionInDB(**response)

    # link updating functions
    async def update_book_links(self, *, book) -> None:
        """
        Accepts dict with keys = 'background_key' and value = 'sharing link'
        Updates table book by keys
        """
        keys = list(book.keys())
        links = list(book.values())
        await self.__update(query=update_book_links_query(keys=keys, links=links))

    # presentation prats
    async def update_presentation_part_links(self, *, prats, presentation: Union['thoery', 'practice'], media_type: Union['image', 'audio']) -> None:
        """
        Accepts dict with keys = 'background_key' and value = 'sharing link'
        Updates table (theory | practice)_(image | audio) by keys
        """
        keys = list(prats.keys())
        links = list(prats.values())
        await self.__update(query=update_presentation_part_links_query(keys=keys, links=links, presentation=presentation, media_type=media_type))


    async def __update(self, query) -> None:
        try:
            response = await self.db.fetch_one(query=query)
        except Exception as e:
            logger.error("--- ERROR RAISED TRYING TO UPDATE PUBLIC ---")
            logger.error(e)
            logger.error("--- ERROR RAISED TRYING TO UPDATE PUBLIC ---")
            raise HTTPException(status_code=400, detail=f"Error raised trying to update public. Exited with {e}")

        return response
