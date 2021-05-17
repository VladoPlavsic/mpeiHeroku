from typing import List, Union
from fastapi import HTTPException

from app.db.repositories.base import BaseDBRepository

from app.db.repositories.public.select.queries import *

from app.models.public import MaterialResponseModel
from app.models.public import MaterialResponse
from app.models.public import BookInDB
from app.models.public import GameInDB
from app.models.public import PresentationInDB
from app.models.public import VideoInDB
from app.models.public import PresentationMediaInDB
from app.models.public import AboutUsInDB
from app.models.public import FAQInDB
from app.models.public import InstructionInDB

from app.models.public import MaterialAllModel
from app.models.public import AudioImagesAllModel

import logging

logger = logging.getLogger(__name__)

class PublicDBSelectRepository(BaseDBRepository):

    async def select_material(self) -> MaterialResponseModel:
        video = await self.__select_video()
        book = await self.__select_book()
        game = await self.__select_game()
        theory = await self.__select_presentation(presentation='theory')
        practice = await self.__select_presentation(presentation='practice')

        return MaterialResponseModel(
            video=video,
            book=book,
            game=game,
            theory=theory,
            practice=practice
        )

    async def select_about_us(self) -> List[AboutUsInDB]:
        response = await self.__select_many(query=select_about_us_query())

        list_ = [AboutUsInDB(**r) for r in response]
        return list_
        

    async def select_faq(self, offset=0, limit=None) -> List[FAQInDB]:
        response = await self.__select_many(query=select_faq_query(offset=offset, limit=limit))

        list_ = [FAQInDB(**r) for r in response]
        return list_

    async def select_instructions(self) -> List[InstructionInDB]:
        response = await self.__select_many(query=select_instruction_query())
        list_ = [InstructionInDB(**r) for r in response]
        return list_

    async def select_all_books(self) -> List[MaterialAllModel]:
        """
        Returns list of id, keys for all books in database
        """
        records = await self.__select_many(query=select_all_material_keys_query(table='book'))

        response = [MaterialAllModel(**record) for record in records] 
        return response       
        
    async def select_all_presentation_parts(self, presentation: Union['theory', 'practice'], media_type: Union['image', 'audio']) -> List[AudioImagesAllModel]:
        """
        Returns list of order, keys for all presentation (theory | practice) parts (image | audio) in database
        """
        records = await self.__select_many(query=select_all_material_part_keys_query(presentation=presentation, media_type=media_type))

        response = [AudioImagesAllModel(**record) for record in records] 
        return response     


    async def __select_book(self) -> BookInDB:
        response = await self.__select_one(query=select_material_query(table='book'), raise_404=False)
        if not response:
            return None
        return BookInDB(**response)


    async def __select_game(self) -> GameInDB:
        response = await self.__select_one(query=select_material_query(table='game'), raise_404=False)
        if not response:
            return None
        return GameInDB(**response)

    async def __select_presentation(self, *, presentation) -> PresentationInDB:
        master = await self.__select_one(query=select_material_query(table=presentation), raise_404=False)
        images = await self.__select_presentation_parts(presentation=presentation, media_type='image')
        audio = await self.__select_presentation_parts(presentation=presentation, media_type='audio')
        if not master:
            return None
        return PresentationInDB(
            **master,
            images=images, 
            audio=audio,)

    async def __select_presentation_parts(self, *, presentation, media_type) -> List[PresentationMediaInDB]:
        medium = await self.__select_many(query=select_material_parts_query(presentation=presentation, media_type=media_type))
        if not medium:
            return []

        response = [PresentationMediaInDB(**r) for r in medium]
        return response

    async def __select_video(self) -> VideoInDB:
        response = await self.__select_one(query=select_material_query(table="video"), raise_404=False)
        if not response:
            return None
        return VideoInDB(**response)

    async def __select_many(self, *, query):
        try:
            response = await self.db.fetch_all(query=query)
        except Exception as e:
            logger.error("--- ERROR TRYING TO SELECT FROM PUBLIC ---")
            logger.error(e)
            logger.error("--- ERROR TRYING TO SELECT FROM PUBLIC ---")
            raise HTTPException(status_code=400, detail=f"Error raised trying to select from public. Exited with {e}")

        return response

    async def __select_one(self, query, raise_404=True):
        try:
            response = await self.db.fetch_one(query=query)
        except Exception as e:
            logger.error("--- SELECT QUERY RAISED UNHANDLED ERROR ---") 
            logger.error(e)
            logger.error("--- SELECT QUERY RAISED UNHANDLED ERROR ---") 
            raise HTTPException(status_code=400, detail=f"Unhandled error raised trying to execute select query {query}. Error {e}")
        
        if not response and raise_404:
            # remove query from fstring before deployment
            raise HTTPException(status_code=404, detail=f"Query found nothing! {query}")

        return response
