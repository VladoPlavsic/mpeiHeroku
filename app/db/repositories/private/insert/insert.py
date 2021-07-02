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
from app.models.private import AnswersInDB
from app.models.private import QuizCreateModel
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
from app.models.private import QuizQuestionInDB
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

        response = await self.__insert(query=query)
        return BookInDB(**response) if content_type == "book" else VideoInDB(**response)

    async def insert_game(self, *, game: GameCreateModel) -> GameInDB:

        response = await self.__insert(query=insert_game_query(fk=game.fk, name_ru=game.name_ru, description=game.description, url=game.url))
        return GameInDB(**response)

    async def insert_quiz_question(self, *, quiz_question: QuizCreateModel) -> QuizQuestionInDB:
        answers = [answer.answer for answer in quiz_question.answers]
        is_true = [answer.is_true for answer in quiz_question.answers]

        response = await self.__insert_many(query=insert_quiz_question_query(
            lecture_id=quiz_question.lecture_id, 
            order_number=quiz_question.order_number, 
            question=quiz_question.question, 
            image_key=quiz_question.image_key, 
            image_url=quiz_question.image_url,
            answers=answers, 
            is_true=is_true,
            )
        )

        answers = [AnswersInDB(**answer) for answer in response]

        return QuizQuestionInDB(**response[0], answers=answers)

    # ### 
    # insert structure
    # ###
    async def insert_grade(self, *, grade: GradeCreateModel) -> GradeInDB:
        query = insert_grades_query(
            name_en=grade.name_en, 
            name_ru=grade.name_ru, 
            background_key=grade.background_key, 
            background=grade.background,
            order_number=grade.order_number,
        )

        response = await self.__insert(query=query)
        return GradeInDB(**response)

    async def insert_subject(self, *, subject: SubjectCreateModel) -> SubjectInDB:
        query = insert_subject_query(
            fk=subject.fk, 
            name_en=subject.name_en, 
            name_ru=subject.name_ru, 
            background_key=subject.background_key, 
            background=subject.background,
            order_number=subject.order_number,
        )

        response = await self.__insert(query=query)
        return SubjectInDB(**response)

    async def insert_branch(self, *, branch: BranchCreateModel) -> BranchInDB:
        query = insert_branch_query(
            fk=branch.fk, 
            name_en=branch.name_en, 
            name_ru=branch.name_ru,
            background_key=branch.background_key,
            background=branch.background,
            order_number=branch.order_number,
        )

        response = await self.__insert(query=query)
        return BranchInDB(**response)

    async def insert_lecture(self, *, lecture: LectureCreateModel) -> LectureInDB:
        query = insert_lecture_query(
            fk=lecture.fk, 
            name_en=lecture.name_en, 
            name_ru=lecture.name_ru, 
            description=lecture.description, 
            background_key=lecture.background_key, 
            background=lecture.background,
            order_number=lecture.order_number,
        )

        response = await self.__insert(query=query)
        return LectureInDB(**response)

        
    # Insert available subscription plans
    # grades
    async def insert_available_grade_plan(self, *, name: str,  price: float, month_count: int) -> None:
        await self.__insert(query=insert_available_grade_plans_query(name=name, price=price, month_count=month_count))

    # subjects
    async def insert_available_subject_plan(self, *, name: str, price: float, month_count: int) -> None:
        await self.__insert(query=insert_available_subject_plans_query(name=name, price=price, month_count=month_count))


    async def __insert(self, *, query) -> Record:
        try:
            response = await self.db.fetch_one(query=query)
        except ForeignKeyViolationError as e:
            logger.error(f"--- ForeignKeyViolationError RAISED TRYING TO INSERT ONE OF PRIVATE QUERIES ---")
            logger.error(e)
            logger.error(f"--- ForeignKeyViolationError RAISED TRYING TO INSERT ONE OF PRIVATE QUERIES ---")
            raise HTTPException(status_code=404, detail=f"Insert query raised ForeignKeyViolationError. No such key in parent table. {query}")
        except Exception as e:
            logger.error(f"--- ERROR RAISED TRYING TO INSERT ONE OF PRIVATE QUERIES ---")
            logger.error(e)
            logger.error(f"--- ERROR RAISED TRYING TO INSERT ONE OF PRIVATE QUERIES---")
            raise HTTPException(status_code=400, detail=f"Unhandled error raised trying to insert one of private queries. Exited with {e}")
        
        return response

    async def __insert_many(self, *, query) -> Record:
        try:
            response = await self.db.fetch_all(query=query)
        except ForeignKeyViolationError as e:
            logger.error(f"--- ForeignKeyViolationError RAISED TRYING TO INSERT ONE OF PRIVATE QUERIES ---")
            logger.error(e)
            logger.error(f"--- ForeignKeyViolationError RAISED TRYING TO INSERT ONE OF PRIVATE QUERIES ---")
            raise HTTPException(status_code=404, detail=f"Insert query raised ForeignKeyViolationError. No such key in parent table. {query}")
        except Exception as e:
            logger.error(f"--- ERROR RAISED TRYING TO INSERT ONE OF PRIVATE QUERIES ---")
            logger.error(e)
            logger.error(f"--- ERROR RAISED TRYING TO INSERT ONE OF PRIVATE QUERIES---")
            raise HTTPException(status_code=400, detail=f"Unhandled error raised trying to insert one of private queries. Exited with {e}")
        
        return response