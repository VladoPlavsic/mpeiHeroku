from typing import Union
from fastapi import HTTPException

from app.db.repositories.public.update.queries import *

from app.db.repositories.base import BaseDBRepository

# update models
from app.models.public import UpdateVideoModel
from app.models.public import UpdateGameModel
from app.models.public import UpdateBookModel
from app.models.public import UpdatePresentationModel
from app.models.public import UpdateAboutUsModel
from app.models.public import UpdateFAQModel
from app.models.public import UpdateInstructionModel

# response models
from app.models.public import VideoInDB
from app.models.public import GameInDB
from app.models.public import BookInDB
from app.models.public import PresentationMasterInDB
from app.models.public import AboutUsInDB
from app.models.public import FAQInDB
from app.models.public import InstructionInDB

from app.db.repositories.types import ContentType

import logging

logger = logging.getLogger(__name__)

class PublicDBUpdateRepository(BaseDBRepository):
    # LINK UPDATING FUNCTIONS
    async def update_book_links(self, *, book) -> None:
        """Updates public book presigned urls by keys.
        
        Keyword arguemts;
        book -- dictionary with:
            key   -- objecy_key
            value -- presigned url 
        """
        keys = list(book.keys())
        links = list(book.values())
        await self._execute_one(query=update_book_links_query(keys=keys, links=links))

    async def update_video_links(self, *, video) -> None:
        """Updates public video presigned urls by keys.
        
        Keyword arguemts;
        video -- dictionary with:
            key   -- objecy_key
            value -- presigned url 
        """
        keys = list(video.keys())
        links = list(video.values())
        await self._execute_one(query=update_video_links_query(keys=keys, links=links))

    async def update_game_links(self, *, game) -> None:
        """Updates public game presigned urls by keys.
        
        Keyword arguemts;
        game -- dictionary with:
            key   -- objecy_key
            value -- presigned url 
        """
        keys = list(game.keys())
        links = list(game.values())
        await self._execute_one(query=update_game_links_query(keys=keys, links=links))

    async def update_quiz_links(self, *, quiz) -> None:
        """Updates public quiz presigned urls by keys.
        
        Keyword arguemts;
        quiz -- dictionary with:
            key   -- objecy_key
            value -- presigned url 
        """
        keys = list(quiz.keys())
        links = list(quiz.values())
        await self._execute_one(query=update_quiz_links_query(keys=keys, links=links))

    async def update_presentation_part_links(self, *, prats, presentation: ContentType, media_type: ContentType) -> None:
        """Updates public presentation presigned urls by keys.
        
        Keyword arguemts;
        parts -- dictionary with:
            key   -- objecy_key
            value -- presigned url 
        presentation -- table name of presentation
        media_type   -- table name of presentation media type
        """
        keys = list(prats.keys())
        links = list(prats.values())
        await self._execute_one(query=update_presentation_part_links_query(keys=keys, links=links, presentation=presentation.value, media_type=media_type.value))

    # METADATA UPDATING FUNCTIONS
    async def update_video(self, *, updated: UpdateVideoModel) -> VideoInDB:
        """Updates public video"""
        response = await self._fetch_one(query=update_video_query(**updated.dict()))
        if not response:
            raise HTTPException(status_code=404, detail="Video not updated, nothing found in public video table.")
        return VideoInDB(**response)

    """ NEW """
    async def update_game(self, *, updated: UpdateGameModel) -> GameInDB:
        """Updates public game"""
        response = await self._fetch_one(query=update_game_query(**updated.dict()))
        if not response:
            raise HTTPException(status_code=404, detail="Game not updated, nothing found in public game table")
        return GameInDB(**response)

    async def update_book(self, updated: UpdateBookModel) -> BookInDB:
        """Updates public book"""
        response = await self._fetch_one(query=update_book_query(**updated.dict()))
        if not response:
            raise HTTPException(status_code=404, detail=f"Book not updated, nothing found for given id {updated.id}")
        return BookInDB(**response)

    async def update_presentation(self, *, updated: UpdatePresentationModel, presentation: ContentType) -> PresentationMasterInDB:
        """Updates public presentation.
        
        Keyword arguments:
        updated      -- updated presentation
        presentation -- ContentType determening table of presentation we want to update. 
        """
        response = await self._fetch_one(query=update_presentation_query(**updated.dict(), presentation=presentation.value))
        if not response:
            raise HTTPException(status_code=404, detail="Presentation not updated!")
        return PresentationMasterInDB(**response)
    """ END NEW """

    async def update_about_us(self, *, updated: UpdateAboutUsModel) -> AboutUsInDB:
        """Updates public about us"""
        response = await self._fetch_one(query=update_about_us_query(**updated.dict()))
        if not response:
            raise HTTPException(status_code=404, detail="About us not updated, nothing found in public about_us table")
        return AboutUsInDB(**response)

    async def update_faq(self, *, updated: UpdateFAQModel) -> FAQInDB:
        """Updates public faq"""
        response = await self._fetch_one(query=update_faq_query(**updated.dict()))
        if not response:
            raise HTTPException(status_code=404, detail="FAQ not updated, nothing found in public faq table")
        return FAQInDB(**response)

    async def update_instruction(self, *, updated: UpdateInstructionModel) -> InstructionInDB:
        """Updates public instructions"""
        response = await self._fetch_one(query=update_instruction_query(**updated.dict()))
        if not response:
            raise HTTPException(status_code=404, detail="Instruction not updated, nothing found in public instruction table")
        return InstructionInDB(**response)

    