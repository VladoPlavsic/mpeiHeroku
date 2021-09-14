from typing import List, Union
from app.db.repositories.base import BaseDBRepository
from app.db.repositories.private.insert.queries import *

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
# offers
from app.models.private import CreateGradeSubscriptionPlan
from app.models.private import CreateSubjectSubscriptionPlan


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

from app.db.repositories.types import ContentType

import logging

logger = logging.getLogger(__name__)

class PrivateDBInsertRepository(BaseDBRepository):
    """Insert data into private db schema."""

    # MATERIAL
    async def insert_theory_check(self, *, fk: int) -> bool:
        """Check if theory can be inserted"""
        response = await self._fetch_one(query=insert_theory_check_query(fk=fk))
        return response['yes']

    async def insert_theory(self, *, presentation: PresentationCreateModel, images: List[PresentationMediaCreate], audio: List[PresentationMediaCreate]) -> PresentationInDB:
        """Tries to insert theory. If successfull, returns formed PresentationInDB model.
        
        Keyword arguments:
        presentation -- PresentationCreateModel
        images       -- List of PresentationMediaCreate, must be not None
        audio        -- List of PresentationMediaCreate, can be left out (audio is not required)
        """
        return await self.__insert_presentation(presentation=presentation, images=images, audio=audio, table=ContentType.THEORY)

    async def insert_practice_check(self, *, fk: int) -> bool:
        """Check if practice can be inserted"""
        response = await self._fetch_one(query=insert_practice_check_query(fk=fk))
        return response['yes']


    async def insert_practice(self, *, presentation: PresentationCreateModel, images: List[PresentationMediaCreate], audio: List[PresentationMediaCreate]) -> PresentationInDB:
        """Tries to insert practice. If successfull, returns formed PresentationInDB model.
        
        Keyword arguments:
        presentation -- PresentationCreateModel
        images       -- List of PresentationMediaCreate, must be not None
        audio        -- List of PresentationMediaCreate, can be left out (audio is not required)
        """
        return await self.__insert_presentation(presentation=presentation, images=images, audio=audio, table=ContentType.PRACTICE)

    async def __insert_presentation(self, *, presentation: PresentationCreateModel, images: List[PresentationMediaCreate], audio: List[PresentationMediaCreate] = None, table: ContentType) -> PresentationInDB:
        """This function inserts all presentation prats.
        
        Keyword arguments:
        presentation -- PresentationCreateModel
        images       -- List of PresentationMediaCreate, must be not None
        audio        -- List of PresentationMediaCreate, can be left out (audio is not required)
        table        -- Content types enum. Determines which type of presentation are we trying to insert.
                        - theory
                        - practice
        """
        query = insert_presentation_query(table=table.value, **presentation.dict())
        presentation_record = await self._fetch_one(query=query)

        query = insert_presentation_media_query(table=table.value, media_type='image', medium=images)
        images_records = await self._fetch_many(query=query)

        images_list = [PresentationMediaInDB(**image) for image in images_records]

        audio_list = []
        if audio:
            query = insert_presentation_media_query(table=table.value, media_type='audio', medium=audio)
            audio_records = await self._fetch_many(query=query)
            audio_list = [PresentationMediaInDB(**audio) for audio in audio_records]

        return PresentationInDB(**presentation_record, images=images_list, audio=audio_list) if presentation_record else None

    async def insert_book_check(self, *, fk: int) -> bool:
        """Check if book can be inserted"""
        response = await self._fetch_one(query=insert_book_check_query(fk=fk))
        return response['yes']

    async def insert_book(self, *, book: BookCreateModel) -> BookInDB:
        """Tries to insert book. If successful returns BookInDB model else None."""
        response = await self._fetch_one(query=insert_book_query(**book.dict()))
        return BookInDB(**response) if response else None

    async def insert_video_check(self, *, fk: int) -> bool:
        """Check if video can be inserted"""
        response = await self._fetch_one(query=insert_video_check_query(fk=fk))
        return response['yes']

    async def insert_video(self, *, video: VideoCreateModel, parse_link=False) -> VideoInDB:
        """Tries to insert video. If successful returns VideoInDB models else None.
        
        Keyword arguments:
        video      -- VideoCreateModel
        parse_link -- (default=False). If you are inserting YouTube video, the link should be parsed using parse_youtube_link function.
                      This way we only store youtube video ID and not whole link, a little bit of data saviour.
        """
        if parse_link:
            video.url = parse_youtube_link(link=video.url)

        response = await self._fetch_one(query=insert_video_query(**video.dict()))
        return VideoInDB(**response) if response else None

    async def insert_game_check(self, *, fk: int) -> bool:
        """Check if game can be inserted"""
        response = await self._fetch_one(query=insert_game_check_query(fk=fk))
        return response['yes']

    async def insert_game(self, *, game: GameCreateModel) -> GameInDB:
        """Tries to insert game. If successful returns GameInDB model else None."""
        response = await self._fetch_one(query=insert_game_query(**game.dict()))
        return GameInDB(**response) if response else None

    async def insert_quiz_check(self, *, fk: int, order_number: int) -> bool:
        """Check if quiz can be inserted"""
        response = await self._fetch_one(query=insert_quiz_check_query(fk=fk, order_number=order_number))
        return response['yes']

    async def insert_quiz_question(self, *, quiz_question: QuizCreateModel) -> QuizQuestionInDB:
        """Tries to insert quiz. If successful returns QuizQuestionInDB model else None."""
        answers = [answer.answer for answer in quiz_question.answers]
        is_true = [answer.is_true for answer in quiz_question.answers]

        quiz_question.answers = answers
        response = await self._fetch_many(query=insert_quiz_question_query(**quiz_question.dict(), is_true=is_true))

        answers = [AnswersInDB(**answer) for answer in response]

        return QuizQuestionInDB(**response[0], answers=answers) if response else None

    # STRUCTURE
    async def insert_grade_check(self, *, name_en: str) -> bool:
        """Check if grade can be inserted"""
        response = await self._fetch_one(query=insert_grade_check_query(name_en=name_en))
        return response['yes']

    async def insert_grade(self, *, grade: GradeCreateModel) -> GradeInDB:
        """ """
        response = await self._fetch_one(query=insert_grades_query(**grade.dict()))
        return GradeInDB(**response) if response else None

    async def insert_subject_check(self, *, fk: int, name_en: str) -> bool:
        """Check if subject can be inserted"""
        response = await self._fetch_one(query=insert_subject_check_query(fk=fk, name_en=name_en))
        return response['yes']

    async def insert_subject(self, *, subject: SubjectCreateModel) -> SubjectInDB:
        """ """
        response = await self._fetch_one(query=insert_subject_query(**subject.dict()))
        return SubjectInDB(**response) if response else None

    async def insert_branch_check(self, *, fk: int, name_en: str) -> bool:
        """Check if branch can be inserted"""
        response = await self._fetch_one(query=insert_branch_check_query(fk=fk, name_en=name_en))
        return response['yes']

    async def insert_branch(self, *, branch: BranchCreateModel) -> BranchInDB:
        """ """
        response = await self._fetch_one(query=insert_branch_query(**branch.dict()))
        return BranchInDB(**response) if response else None

    async def insert_lecture_check(self, *, fk: int, name_en: str) -> bool:
        """Check if lecture can be inserted"""
        response = await self._fetch_one(query=insert_lecture_check_query(fk=fk, name_en=name_en))
        return response['yes']

    async def insert_lecture(self, *, lecture: LectureCreateModel) -> LectureInDB:
        """ """
        response = await self._fetch_one(query=insert_lecture_query(**lecture.dict()))
        return LectureInDB(**response) if response else None

        
    # PLANS
    async def insert_available_grade_plan(self, *, grade_plan: CreateGradeSubscriptionPlan) -> None:
        """ """
        await self._execute_one(query=insert_available_grade_plans_query(**grade_plan.dict()))

    async def insert_available_subject_plan(self, *, subject_plan: CreateSubjectSubscriptionPlan) -> None:
        """ """
        await self._execute_one(query=insert_available_subject_plans_query(**subject_plan.dict()))
