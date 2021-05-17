from typing import List, Union
from databases.backends.postgres import Record
from app.db.repositories.base import BaseDBRepository
from app.db.repositories.private.insert.queries import *
from asyncpg.exceptions import ForeignKeyViolationError


from fastapi import HTTPException

# parsers
from app.db.repositories.parsers import parse_youtube_link

# ###
# create models
# ###
# material
from app.models.private import PresentationCreateModel, PresentationMediaCreate
from app.models.private import BookCreateModel
from app.models.private import VideoCreateModel
from app.models.private import GameCreateModel
# structure
from app.models.private import GradeCreateModel
from app.models.private import SubjectCreateModel
from app.models.private import BranchCreateModel
from app.models.private import LectureCreateModel


# ###
# response models
# ###
# material
from app.models.private import PresentationInDB, PresentationMediaInDB
from app.models.private import BookInDB
from app.models.private import VideoInDB
from app.models.private import GameInDB
# structure
from app.models.private import GradeInDB
from app.models.private import SubjectInDB
from app.models.private import BranchInDB
from app.models.private import LectureInDB

import logging

logger = logging.getLogger(__name__)

class PrivateDBInsertRepository(BaseDBRepository):

    # ###
    # insert material
    # ###
    async def check_timestamp_is_set(self) -> bool:
        response = await self.db.fetch_one(query=check_timestamp_is_set_query())
        if response['count'] == 0:
            await self.__set_timestamp_to_now()

    async def __set_timestamp_to_now(self) -> None:
        '''
        Only to be used in case if there is not timestamp in the table. So first do check to see if there is one, and if not call this function.
        I can't stress this enough!
        '''
        await self.db.fetch_one(query=set_timestamp_to_now_query())

    async def insert_theory(self, *, presentation: PresentationCreateModel, images: List[PresentationMediaCreate], audio: List[PresentationMediaCreate]) -> PresentationInDB:
        return await self.__insert_presentation(presentation=presentation, images=images, audio=audio, table='theory')

    async def insert_practice(self, *, presentation: PresentationCreateModel, images: List[PresentationMediaCreate], audio: List[PresentationMediaCreate]) -> PresentationInDB:
        return await self.__insert_presentation(presentation=presentation, images=images, audio=audio, table='practice')

    async def __insert_presentation(self, *, presentation: PresentationCreateModel, images: List[PresentationMediaCreate], audio: List[PresentationMediaCreate], table: Union['theory', 'practice']) -> PresentationInDB:
        
        query = insert_presentation_query(
            presentation=table, 
            fk=presentation.fk,
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


        except ForeignKeyViolationError as e:
            logger.error(f"--- ForeignKeyViolationError RAISED TRYING TO INSERT {table} ---")
            logger.error(e)
            logger.error(f"--- ForeignKeyViolationError RAISED TRYING TO INSERT {table} ---")
            raise HTTPException(status_code=404, detail=f"Insert {table} raised ForeignKeyViolationError. No such key in table lectures.")
        except Exception as e:
            logger.error(f"--- ERROR RAISED TRYING TO INSERT {table} ---")
            logger.error(e)
            logger.error(f"--- ERROR RAISED TRYING TO INSERT {table} ---")
            raise HTTPException(status_code=400, detail=f"Unhandled error raised trying to insert {table}. Exited with {e}")
            
        # check if timestamp is set, set if not
        await self.check_timestamp_is_set()

        return PresentationInDB(
            id=inserted_presentation['id'], 
            name_ru=inserted_presentation['name_ru'], 
            description=inserted_presentation['description'], 
            images=images,
            audio=audios)

    async def insert_book(self, *, book: BookCreateModel) -> BookInDB:
        return await self.__insert_book_video(material=book, content_type="book")

    async def insert_video(self, *, video: VideoCreateModel, parse_link=False) -> VideoInDB:
        '''
        parse_link: if inserting youtube video, link should be parsed and retrived
        only id part for embeding it
        '''
        if parse_link:
            video.url = parse_youtube_link(link=video.url)

        return await self.__insert_book_video(material=video, content_type="video")

    async def __insert_book_video(self, *, material: Union[BookCreateModel, VideoCreateModel], content_type: Union["book", "video"]) -> Union[BookInDB, VideoInDB]:

        if content_type == "video":
            query = insert_video_query(fk=material.fk, name_ru=material.name_ru, description=material.description, key=material.key, url=material.url)
        elif content_type == "book":
            query = insert_book_query(fk=material.fk, name_ru=material.name_ru, description=material.description, key=material.key, url=material.url)

        try:
            inserted = await self.db.fetch_one(query=query)
        except ForeignKeyViolationError as e:
            logger.error(f"--- ForeignKeyViolationError RAISED TRYING TO INSERT {content_type} ---")
            logger.error(e)
            logger.error(f"--- ForeignKeyViolationError RAISED TRYING TO INSERT {content_type} ---")
            raise HTTPException(status_code=404, detail=f"Insert {content_type} raised ForeignKeyViolationError. No such key in table lectures.")
        except Exception as e:
            logger.error(f"--- ERROR RAISED TRYING TO INSERT {content_type} ---")
            logger.error(e)
            logger.error(f"--- ERROR RAISED TRYING TO INSERT {content_type} ---")
            raise HTTPException(status_code=400, detail=f"Unhandled error raised trying to insert {content_type}. Exited with {e}")

        # check if timestamp is set, set if not
        await self.check_timestamp_is_set()

        return BookInDB(**inserted) if content_type == "book" else VideoInDB(**inserted)

    async def insert_game(self, *, game: GameCreateModel) -> GameInDB:

        query = insert_game_query(fk=game.fk, name_ru=game.name_ru, description=game.description, url=game.url)

        try:
            inserted = await self.db.fetch_one(query=query)
        except ForeignKeyViolationError as e:
            logger.error(f"--- ForeignKeyViolationError RAISED TRYING TO INSERT GAME ---")
            logger.error(e)
            logger.error(f"--- ForeignKeyViolationError RAISED TRYING TO INSERT GAME ---")
            raise HTTPException(status_code=404, detail=f"Insert game raised ForeignKeyViolationError. No such key in table lectures.")
        except Exception as e:
            logger.error(f"--- ERROR RAISED TRYING TO INSERT GAME ---")
            logger.error(e)
            logger.error(f"--- ERROR RAISED TRYING TO INSERT GAME ---")
            raise HTTPException(status_code=400, detail=f"Unhandled error raised trying to insert book. Exited with {e}")

        # check if timestamp is set, set if not
        await self.check_timestamp_is_set()

        return GameInDB(**inserted)


    # ### 
    # insert structure
    # ###
    async def insert_grade(self, *, grade: GradeCreateModel) -> GradeInDB:
        query = insert_grades_query(
            name_en=grade.name_en, 
            name_ru=grade.name_ru, 
            background_key=grade.background_key, 
            background=grade.background
        )

        response = await self.__insert_structure(query=query)
        return GradeInDB(**response)

    async def insert_subject(self, *, subject: SubjectCreateModel) -> SubjectInDB:
        query = insert_subject_query(
            fk=subject.fk, 
            name_en=subject.name_en, 
            name_ru=subject.name_ru, 
            background_key=subject.background_key, 
            background=subject.background
        )

        response = await self.__insert_structure(query=query)
        return SubjectInDB(**response)

    async def insert_branch(self, *, branch: BranchCreateModel) -> BranchInDB:
        query = insert_branch_query(
            fk=branch.fk, 
            name_en=branch.name_en, 
            name_ru=branch.name_ru,
            background_key=branch.background_key, 
            background=branch.background
        )

        response = await self.__insert_structure(query=query)
        return BranchInDB(**response)

    async def insert_lecture(self, *, lecture: LectureCreateModel) -> LectureInDB:
        query = insert_lecture_query(
            fk=lecture.fk, 
            name_en=lecture.name_en, 
            name_ru=lecture.name_ru, 
            description=lecture.description, 
            background_key=lecture.background_key, 
            background=lecture.background,
        )

        response = await self.__insert_structure(query=query)
        return LectureInDB(**response)

    async def __insert_structure(self, *, query) -> Record:
        try:
            response = await self.db.fetch_one(query=query)
        except ForeignKeyViolationError as e:
            logger.error(f"--- ForeignKeyViolationError RAISED TRYING TO INSERT ONE OF STRUCTURAL QUERIES ---")
            logger.error(e)
            logger.error(f"--- ForeignKeyViolationError RAISED TRYING TO INSERT ONE OF STRUCTURAL QUERIES ---")
            raise HTTPException(status_code=404, detail=f"Insert query raised ForeignKeyViolationError. No such key in parent table. {query}")
        except Exception as e:
            logger.error(f"--- ERROR RAISED TRYING TO INSERT ONE OF STRUCTURAL QUERIES ---")
            logger.error(e)
            logger.error(f"--- ERROR RAISED TRYING TO INSERT ONE OF STRUCTURAL QUERIES ---")
            raise HTTPException(status_code=400, detail=f"Unhandled error raised trying to insert one of structural queries. Exited with {e}")
        
        # check if timestamp is set, set if not
        await self.check_timestamp_is_set()

        return response
        
        