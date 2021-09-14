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
from app.models.public import QuizInDB, QuizQuestionInDB, AnswersInDB, QuizGetResultsModel, QuizResults, QuizQuestionAnswerCorrectPair
from app.models.public import PresentationMediaInDB
from app.models.public import AboutUsInDB
from app.models.public import FAQInDB
from app.models.public import InstructionInDB

from app.models.public import MaterialAllModel
from app.models.public import AudioImagesAllModel

from app.db.repositories.types import ContentType

import logging

logger = logging.getLogger(__name__)

class PublicDBSelectRepository(BaseDBRepository):

    async def select_material(self) -> MaterialResponseModel:
        """Returns all material from schema public."""
        video = await self.select_video()
        book = await self.select_book()
        game = await self.select_game()
        quiz = await self.select_quiz()
        theory = await self.select_presentation(presentation=ContentType.THEORY)
        practice = await self.select_presentation(presentation=ContentType.PRACTICE)

        return MaterialResponseModel(
            video=video,
            book=book,
            game=game,
            quiz=quiz,
            theory=theory,
            practice=practice
        )

    async def select_about_us(self) -> List[AboutUsInDB]:
        """Returns all about us."""
        records = await self._fetch_many(query=select_about_us_query())
        return [AboutUsInDB(**record) for record in records]

    async def select_faq(self, offset=0, limit=None) -> List[FAQInDB]:
        """Returns frequently asked questions.
        
        Keyword arguments:
        offset -- offset from which we should start listing questions
        limi   -- limit how much questions to list
        """
        records = await self._fetch_many(query=select_faq_query(offset=offset, limit=limit))
        return [FAQInDB(**record) for record in records]

    async def select_instructions(self) -> List[InstructionInDB]:
        """Returns all instructions."""
        records = await self._fetch_many(query=select_instruction_query())
        return [InstructionInDB(**record) for record in records]

    async def select_all_presentation_parts(self, presentation: ContentType, media_type:ContentType) -> List[AudioImagesAllModel]:
        """Returns list of order, object_keys for all presentation (theory || practice) parts (images|| audio) in database schema public"""
        records = await self._fetch_many(query=select_all_material_part_keys_query(presentation=presentation.value, media_type=media_type.value))
        return [AudioImagesAllModel(**record) for record in records]      

    async def select_book(self) -> BookInDB:
        """Returns a BookInDB from schema public"""
        response = await self._fetch_one(query=select_material_query(table=ContentType.BOOK.value))
        return BookInDB(**response) if response else None

    async def select_all_books(self) -> List[MaterialAllModel]:
        """Returns list of object_keys for all books in database schema public"""
        records = await self._fetch_many(query=select_all_material_keys_query(table=ContentType.BOOK.value))
        return [MaterialAllModel(**record) for record in records]        

    async def select_game(self) -> GameInDB:
        """Returns GameInDB from schema public"""
        response = await self._fetch_one(query=select_material_query(table=ContentType.GAME.value))
        return GameInDB(**response) if response else None

    async def select_all_game(self) -> List[MaterialAllModel]:
        """Returns list of object_keys for all game in dabases, schema public"""
        records = await self._fetch_many(query=select_all_material_keys_query(table=ContentType.GAME.value))
        return [MaterialAllModel(**record) for record in records]

    async def select_quiz(self) -> QuizInDB:
        """Returns QuizInDB stored in public schema. If there is no quiz, return None."""
        responses = await self._fetch_many(query=select_quiz_questions_query())

        questions = [QuizQuestionInDB(**response, answers=[]) for response in responses]
        for question in questions:
            responses = await self._fetch_many(query=select_quiz_answers_query(fk=question.id))
            question.answers = [AnswersInDB(**response) for response in responses]

        return QuizInDB(questions=questions) if questions else None

    async def select_all_quiz(self) -> List[MaterialAllModel]:
        """Returns list of object_keys for all quizes in database, schema public"""
        records = await self._fetch_many(query=select_all_material_keys_query(table="quiz_question"))
        return [MaterialAllModel(**record) for record in records if record['object_key']]

    async def select_video(self) -> VideoInDB:
        """Returns VideInDB from schema public"""
        response = await self._fetch_one(query=select_material_query(table=ContentType.VIDEO.value))
        return VideoInDB(**response) if response else None

    async def select_all_video(self) -> List[MaterialAllModel]:
        """Returns list of object_keys for all video in database schema public"""
        records = await self._fetch_many(query=select_all_material_keys_query(table=ContentType.VIDEO.value))
        return [MaterialAllModel(**record) for record in records if record['object_key']]

    async def select_presentation(self, *, presentation: ContentType) -> PresentationInDB:
        """Return presentation data - PresentationInDB based on presentation type."""
        master = await self._fetch_one(query=select_material_query(table=presentation.value))
        images = await self.__select_presentation_parts(presentation=presentation, media_type=ContentType.IMAGE)
        audio = await self.__select_presentation_parts(presentation=presentation, media_type=ContentType.AUDIO)
        return PresentationInDB(**master, images=images, audio=audio) if master else None

    async def __select_presentation_parts(self, *, presentation: ContentType, media_type: ContentType) -> List[PresentationMediaInDB]:
        """Return PresentationMediaInDB based on presentation and media type they belong to."""
        medium = await self._fetch_many(query=select_material_parts_query(presentation=presentation.value, media_type=media_type.value))
        return [PresentationMediaInDB(**media) for media in medium]

    async def check_quiz_results(self, *, quiz_results: QuizGetResultsModel) -> QuizResults:
        """Checks quiz results, and returns QuizResults object."""
        questions = []
        answers = []
        for result in quiz_results.results:
            questions.append(result.question)
            answers.append(result.answer)

        records = await self._fetch_one(query=check_quiz_results_query(questions=questions, answers=answers))
        response = []

        for index in range(0, len(records['question_ids'])):
            response.append(QuizQuestionAnswerCorrectPair(
                question_id=records['question_ids'][index],
                answer_id=records['answer_ids'][index],
                question_number=records['question_numbers'][index],
                answer=records['answers'][index],
                correct=records['correct'][index],
                correct_answer=records['correct_answers'][index],
                correct_answer_id=records['correct_answers_id'][index],
            ))

        return QuizResults(results=response)
