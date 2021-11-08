from typing import Union
from fastapi import HTTPException

from app.db.repositories.base import BaseDBRepository

from app.db.repositories.public.insert.queries import *

from app.db.repositories.parsers import *

# insert models
from app.models.public import VideoCreateModel
from app.models.public import IntroVideoCreateModel
from app.models.public import GameCreateModel
from app.models.public import BookCreateModel
from app.models.public import PresentationCreateModel
from app.models.public import PresentationMediaCreate
from app.models.public import QuizCreateModel
from app.models.public import AnswersInDB
from app.models.public import AboutUsCreateModel
from app.models.public import FAQCreateModel
from app.models.public import InstructionCreateModel
from app.models.public import ReviewCreateModel

# response models
from app.models.public import VideoInDB
from app.models.public import IntroVideoInDB
from app.models.public import GameInDB
from app.models.public import BookInDB
from app.models.public import PresentationInDB
from app.models.public import PresentationMediaInDB
from app.models.public import QuizQuestionInDB
from app.models.public import AboutUsInDB
from app.models.public import FAQInDB
from app.models.public import InstructionInDB
from app.models.public import ReviewInDB

from app.db.repositories.types import ContentType

import logging

logger = logging.getLogger(__name__)

class PublicDBInsertRepository(BaseDBRepository):
    """Insert data into public db schema."""

    async def insert_video(self, *, video: VideoCreateModel, parse_link=False) -> VideoInDB:
        """Tries to insert video. If successful returns VideoInDB model else None.
        
        Keyword arguments:
        video      -- VideoCreateModel
        parse_link -- (default=False). If you are inserting YouTube video, the link should be parsed using parse_youtube_link function.
                      This way we only store youtube video ID and not whole link, a little bit of data saviour.
        """
        if parse_link:
            video.url = parse_youtube_link(link=video.url)

        response = await self._fetch_one(query=insert_video_query(**video.dict()))
        return VideoInDB(**response) if response else None

    async def insert_intro_video(self, *, video: IntroVideoCreateModel, parse_link=False) -> IntroVideoInDB:
        """Same as insert video, only different table."""
        if parse_link:
            video.url = parse_youtube_link(link=video.url)
        
        response = await self._fetch_one(query=insert_intro_video_query(**video.dict()))
        return IntroVideoInDB(**response) if response else None

    async def insert_game(self, *, game: GameCreateModel) -> GameInDB:
        """Tries to insert game. If successful returns GameInDB model else None."""
        response = await self._fetch_one(query=insert_game_query(**game.dict()))
        return GameInDB(**response) if response else None

    async def insert_book(self, *, book: BookCreateModel) -> BookInDB:
        """Tries to insert book. If successful returns BookInDB model else None."""
        response = await self._fetch_one(query=insert_book_query(**book.dict()))
        return BookInDB(**response) if response else None

    async def insert_theory(self, *, presentation: PresentationCreateModel, images: List[PresentationMediaCreate], audio: List[PresentationMediaCreate]) -> PresentationInDB:
        """Tries to insert theory. If successfull, returns formed PresentationInDB model.
        
        Keyword arguments:
        presentation -- PresentationCreateModel
        images       -- List of PresentationMediaCreate, must be not None
        audio        -- List of PresentationMediaCreate, can be left out (audio is not required)
        """
        return await self.__insert_presentation(presentation=presentation, images=images, audio=audio, table=ContentType.THEORY)

    async def insert_practice(self, *, presentation: PresentationCreateModel, images: List[PresentationMediaCreate], audio: List[PresentationMediaCreate]) -> PresentationInDB:
        """Tries to insert practice. If successfull, returns formed PresentationInDB model.
        
        Keyword arguments:
        presentation -- PresentationCreateModel
        images       -- List of PresentationMediaCreate, must be not None
        audio        -- List of PresentationMediaCreate, can be left out (audio is not required)
        """
        return await self.__insert_presentation(presentation=presentation, images=images, audio=audio, table=ContentType.PRACTICE)

    async def __insert_presentation(self, *, presentation: PresentationCreateModel, images: List[PresentationMediaCreate], audio: List[PresentationMediaCreate], table: ContentType) -> PresentationInDB:
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

        image_list = [PresentationMediaInDB(**image) for image in images_records]

        audio_list = []
        if audio:
            query = insert_presentation_media_query(table=table.value, media_type="audio", medium=audio)
            audio_records = await self._fetch_many(query=query)
            audio_list = [PresentationMediaInDB(**audio) for audio in audio_records]

        return PresentationInDB(**presentation_record, images=image_list, audio=audio_list)

    async def insert_quiz_question(self, *, quiz_question: QuizCreateModel) -> QuizQuestionInDB:
        """Tries to insert quiz. If successful returns QuizQuestionInDB model else None."""
        answers = [answer.answer for answer in quiz_question.answers]
        is_true = [answer.is_true for answer in quiz_question.answers]

        quiz_question.answers = answers
        response = await self._fetch_many(query=insert_quiz_question_query(**quiz_question.dict(), is_true=is_true))
        
        answers = [AnswersInDB(**answer) for answer in response]
        
        return QuizQuestionInDB(**response[0], answers=answers) if response else None

    async def insert_about_us(self, *, about_us: AboutUsCreateModel) -> AboutUsInDB:
        """Tries to insert about us. If successful returns AboutUsInDB model else None."""
        response = await self._fetch_one(query=insert_about_us_query(**about_us.dict()))
        return AboutUsInDB(**response) if response else None

    async def insert_faq(self, *, faq: FAQCreateModel) -> FAQInDB:
        """Tries to insert faq. If successful returns FAQInDB model else None."""
        response = await self._fetch_one(query=insert_faq_query(**faq.dict()))
        return FAQInDB(**response) if response else None

    async def insert_instruction(self, *, instruction: InstructionCreateModel) -> InstructionInDB:
        """Tries to insert instruction. If successful returns InstructionInDB model else None."""
        response = await self._fetch_one(query=insert_instruction_query(**instruction.dict()))
        return InstructionInDB(**response) if response else None

    async def insert_review(self, *, review: ReviewCreateModel) -> ReviewInDB:
        """Tries to insert review. If successfull returns ReviewInDB model else None"""
        response = await self._fetch_one(query=insert_review_query(**review.dict()))
        return ReviewInDB(**response) if response else None

