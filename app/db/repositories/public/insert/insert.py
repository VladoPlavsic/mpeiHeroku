from typing import Union
from fastapi import HTTPException

from app.db.repositories.base import BaseDBRepository

from app.db.repositories.public.insert.queries import *

from app.db.repositories.parsers import *

# insert models
from app.models.public import VideoCreateModel
from app.models.public import GameCreateModel
from app.models.public import BookCreateModel
from app.models.public import PresentationCreateModel
from app.models.public import PresentationMediaCreate
from app.models.public import AboutUsCreateModel
from app.models.public import FAQCreateModel
from app.models.public import InstructionCreateModel

# response models
from app.models.public import VideoInDB
from app.models.public import GameInDB
from app.models.public import BookInDB
from app.models.public import PresentationInDB
from app.models.public import PresentationMediaInDB
from app.models.public import AboutUsInDB
from app.models.public import FAQInDB
from app.models.public import InstructionInDB

import logging

logger = logging.getLogger(__name__)


class PublicDBInsertRepository(BaseDBRepository):

    async def insert_video(self, *, video: VideoCreateModel, parse_link=False) -> VideoInDB:
        if parse_link:
            video.url = parse_youtube_link(link=video.url)
        response = await self.__insert(query=insert_video_query(name_ru=video.name_ru, url=video.url, description=video.description))
        return VideoInDB(**response)

    async def insert_game(self, *, game: GameCreateModel) -> GameInDB:
        response = await self.__insert(query=insert_game_query(name_ru=game.name_ru, url=game.url, description=game.description))
        return GameInDB(**response)

    async def insert_book(self, *, book: BookCreateModel) -> BookInDB:
        response = await self.__insert(query=insert_book_query(name_ru=book.name_ru, url=book.url, description=book.description, key=book.key))
        return BookInDB(**response)

    async def insert_theory(self, *, presentation: PresentationCreateModel, images: List[PresentationMediaCreate], audio: List[PresentationMediaCreate]) -> PresentationInDB:
        return await self.__insert_presentation(presentation=presentation, images=images, audio=audio, table='theory')

    async def insert_practice(self, *, presentation: PresentationCreateModel, images: List[PresentationMediaCreate], audio: List[PresentationMediaCreate]) -> PresentationInDB:
        return await self.__insert_presentation(presentation=presentation, images=images, audio=audio, table='practice')

    async def __insert_presentation(self, *, presentation: PresentationCreateModel, images: List[PresentationMediaCreate], audio: List[PresentationMediaCreate], table: Union['theory', 'practice']) -> PresentationInDB:
        
        query = insert_presentation_query(
            presentation=table, 
            name_ru=presentation.name_ru,
            description=presentation.description,
            key=presentation.key)

        images_query = insert_presentation_media_query(
            presentation=table,
            media_type='image',
            medium=images,
        )

        if audio:
            audio_query = insert_presentation_media_query(
                presentation=table,
                media_type='audio',
                medium=audio,
            )

        try:
            inserted_presentation = await self.db.fetch_one(query=query)
            inserted_images = await self.db.fetch_all(query=images_query)

            if audio:
                inserted_audio = await self.db.fetch_all(query=audio_query) 

            images = []
            audios = []
            for image in inserted_images:
                images.append(PresentationMediaInDB(**image))
                
            if audio:
                for audio in inserted_audio:
                    audios.append(PresentationMediaInDB(**audio))

        except Exception as e:
            logger.error(f"--- ERROR RAISED TRYING TO INSERT {table} ---")
            logger.error(e)
            logger.error(f"--- ERROR RAISED TRYING TO INSERT {table} ---")
            raise HTTPException(status_code=400, detail=f"Unhandled error raised trying to insert {table}. Exited with {e}")
            
        return PresentationInDB(
            key=inserted_presentation['key'],
            name_ru=inserted_presentation['name_ru'], 
            description=inserted_presentation['description'], 
            images=images,
            audio=audios)


    async def insert_about_us(self, *, about_us: AboutUsCreateModel) -> AboutUsInDB:
        response = await self.__insert(query=insert_about_us_query(order_num=about_us.order, title=about_us.title, description=about_us.description, svg=about_us.svg))
        return AboutUsInDB(**response)

    async def insert_faq(self, *, faq: FAQCreateModel) -> FAQInDB:
        response = await self.__insert(query=insert_faq_query(question=faq.question, answer=faq.answer))
        return FAQInDB(**response)

    async def insert_instruction(self, *, instruction: InstructionCreateModel) -> InstructionInDB:
        response = await self.__insert(query=insert_instruction_query(order_num=instruction.order, title=instruction.title, description=instruction.description))
        return InstructionInDB(**response)

    async def __insert(self, *, query) -> None:
        try:
            response = await self.db.fetch_one(query=query)
        except Exception as e:
            logger.error("--- ERROR TRYING TO INSERT ---")
            logger.error(e)
            logger.error("--- ERROR TRYING TO INSERT ---")
            raise HTTPException(status_code=400, detail=f"Error raised trying to insert public content. Exited with {e}")

        return response
