from typing import List, Tuple, Union
from app.db.repositories.base import BaseDBRepository
from fastapi import HTTPException

# queries
from app.db.repositories.private.select.queries import *

# response models
from app.models.private import GradeInDB
from app.models.private import SubjectInDB
from app.models.private import BranchInDB
from app.models.private import LectureInDB
from app.models.private import MaterialResponseModel

from app.models.user import UserAvailableGrades
from app.models.user import UserAvailableSubjects

from app.models.private import VideoInDB
from app.models.private import GameInDB
from app.models.private import BookInDB
from app.models.private import QuizInDB, QuizQuestionInDB, AnswersInDB, QuizGetResultsModel, QuizResults, QuizQuestionAnswerCorrectPair
from app.models.private import PresentationInDB
from app.models.private import PresentationMediaInDB

from app.models.private import StructureAllModel
from app.models.private import MaterialAllModel
from app.models.private import AudioImagesAllModel

# offers
from app.models.private import AvailableGradeSubscriptionOffers
from app.models.private import AvailableSubjectSubscriptionOffers
# plans
from app.models.private import AvailableGradeSubscriptionPlans
from app.models.private import AvailableSubjectSubscriptionPlans



import logging

logger = logging.getLogger(__name__)

class PrivateDBSelectRepository(BaseDBRepository):

    async def get_grade_by_name(self, *, grade_name) -> GradeInDB:
        
        response = await self.__select_one(query=get_grade_by_name_query(grade_name=grade_name))

        return GradeInDB(**response)

    async def get_subject_by_name(self, *, grade_name, subject_name) -> Tuple[SubjectInDB, str]:
        # get grade id (fk for subject)
        grade = await self.get_grade_by_name(grade_name=grade_name)

        response = await self.__select_one(query=get_subject_by_name_query(fk=grade.id, subject_name=subject_name))
        return SubjectInDB(**response), grade.name_ru

    async def get_branch_by_name(self, *, grade_name, subject_name, branch_name) -> Tuple[BranchInDB, str]:
        # get subject id (fk for branch)
        (subject, path) = await self.get_subject_by_name(grade_name=grade_name, subject_name=subject_name)

        response = await self.__select_one(query=get_branch_by_name_query(fk=subject.id, branch_name=branch_name))
        return BranchInDB(**response), path + '/' + subject.name_ru

    async def get_lecture_by_name(self, *, grade_name, subject_name, branch_name, lecture_name) -> Tuple[LectureInDB, str]:
        # get branch id (fk for lecture)
        (branch, path) = await self.get_branch_by_name(grade_name=grade_name, subject_name=subject_name, branch_name=branch_name)

        response = await self.__select_one(query=get_lecture_by_name_query(fk=branch.id, lecture_name=lecture_name))
        return LectureInDB(**response), path + '/' + branch.name_ru

    async def select_grades(self, *, ids=None) -> List[GradeInDB]:
        """
        Returns list of grades available to customer, or all of them in ids=None
        ids - list of grade ids available to customer
        """
        response_data = await self.__select_many(query=select_grades_query(ids=ids))

        response = []
        for data in response_data:
            response.append(GradeInDB(**data))

        return response        

    async def select_all_grades(self) -> List[StructureAllModel]:
        """
        Returns list of id, background_keys for all grades in database
        """
        records = await self.__select_many(query=select_all_grade_keys_query())

        response = [StructureAllModel(**record) for record in records] 
        return response       

    async def select_subjects(self, *, fk, ids=None) -> List[SubjectInDB]:
        """
        Returns list of subjects available to customer, or all of them in ids=None
        ids - list of subject ids available to customer
        """
        response_data = await self.__select_many(query=select_subject_query(fk=fk, ids=ids))

        response = []
        for data in response_data:
            response.append(SubjectInDB(**data))

        return response

    async def select_all_subjects(self) -> List[StructureAllModel]:
        """
        Returns list of id, background_keys for all subjects in database
        """
        records = await self.__select_many(query=select_all_subject_keys_query())

        response = [StructureAllModel(**record) for record in records] 
        return response       

    async def select_branches(self, *, fk) -> List[BranchInDB]:

        response_data = await self.__select_many(query=select_branch_query(fk=fk))

        response = []
        for data in response_data:
            response.append(BranchInDB(**data))

        return response

    async def select_all_branches(self) -> List[StructureAllModel]:
        """
        Returns list of id, background_keys for all branches in database
        """
        records = await self.__select_many(query=select_all_branch_keys_query())

        response = [StructureAllModel(**record) for record in records] 
        return response       

    async def select_lectures(self, *, fk) -> List[LectureInDB]:

        response_data = await self.__select_many(query=select_lecture_query(fk=fk))

        response = []
        for data in response_data:
            response.append(LectureInDB(**data))

        return response

    async def select_all_lectures(self) -> List[StructureAllModel]:
        """
        Returns list of id, background_keys for all lectures in database
        """
        records = await self.__select_many(query=select_all_lecture_keys_query())

        response = [StructureAllModel(**record) for record in records] 
        return response       

    async def select_material(self, *, fk) -> MaterialResponseModel:
        #response = await self.__select_one(query=select_material_query(fk=fk))
        #material = MaterialBulk(**response)

        video = await self.select_video(fk=fk)
        book = await self.select_book(fk=fk)
        game = await self.select_game(fk=fk)
        quiz = await self.select_quiz(fk=fk)
        theory = await self.select_presentation(fk=fk, presentation='theory')
        practice = await self.select_presentation(fk=fk, presentation='practice')

        return MaterialResponseModel(
            video=video,
            book=book,
            game=game,
            quiz=quiz,
            theory=theory,
            practice=practice
        )

    async def select_video(self, *, fk) -> VideoInDB:
        response = await self.__select_one(query=select_one_material_query(fk=fk, table='video'), raise_404=False)
        if not response:
            return None
        return VideoInDB(**response)

    async def select_quiz(self, *, fk) -> QuizInDB:
        resposnes = await self.__select_many(query=select_quiz_questions_query(fk=fk))

        questions = [QuizQuestionInDB(**response, answers=[]) for response in resposnes]
        for question in questions:
            responses = await self.__select_many(query=select_quiz_answers_query(fk=question.id))
            question.answers = [AnswersInDB(**response) for response in responses]

        return QuizInDB(questions=questions) if len(questions) > 0 else None

    async def check_quiz_results(self, *, quiz_results: QuizGetResultsModel) -> QuizResults:
        questions = []
        answers = []
        for result in quiz_results.results:
            questions.append(result.question)
            answers.append(result.answer)

        records = await self.__select_one(query=check_quiz_results_query(questions=questions, answers=answers))
        response = []

        for index in range(0, len(records['question_ids'])):
            response.append(QuizQuestionAnswerCorrectPair(
                question_id=records['question_ids'][index],
                answer_id=records['answer_ids'][index],
                question_number=records['question_numbers'][index],
                answer=records['answers'][index],
                correct=records['correct'][index],
                correct_answer=records['correct_answers'][index],
            ))

        return QuizResults(results=response, lecture_id=quiz_results.lecture_id)

    async def select_all_video(self) -> List[MaterialAllModel]:
        """
        Returns list of id, keys for all video in database
        """
        records = await self.__select_many(query=select_all_material_keys_query(table='video'))

        response = [MaterialAllModel(**record) for record in records if record['key']]
        return response

    async def select_all_quiz(self) -> List[MaterialAllModel]:
        """
        Returns list of id, keys for all quizes in database
        """
        records = await self.__select_many(query=select_all_material_keys_query(table='quiz_question'))

        response = [MaterialAllModel(**record) for record in records if record['key']]
        return response

    async def select_book(self, *, fk) -> BookInDB:
        response = await self.__select_one(query=select_one_material_query(fk=fk, table='book'), raise_404=False)
        if not response:
            return None
        return BookInDB(**response)

    async def select_all_books(self) -> List[MaterialAllModel]:
        """
        Returns list of id, keys for all books in database
        """
        records = await self.__select_many(query=select_all_material_keys_query(table='book'))

        response = [MaterialAllModel(**record) for record in records] 
        return response       

    async def select_game(self, *, fk) -> GameInDB:
        response = await self.__select_one(query=select_one_material_query(fk=fk, table='game'), raise_404=False)
        if not response:
            return None
        return GameInDB(**response)

    async def select_presentation(self, *, fk, presentation) -> PresentationInDB:
        master = await self.__select_one(query=select_one_material_query(fk=fk, table=presentation), raise_404=False)
        images = await self.select_presentation_parts(fk=fk, presentation=presentation, media_type='image')
        audio = await self.select_presentation_parts(fk=fk, presentation=presentation, media_type='audio')
        if not master:
            return None
        return PresentationInDB(
            **master,
            images=images, 
            audio=audio,)

    async def select_all_presentation(self, presentation) -> List[MaterialAllModel]:
        """
        Returns list of id, keys for all presentation (theory | practice) in database
        """
        records = await self.__select_many(query=select_all_material_keys_query(table=presentation))

        response = [MaterialAllModel(**record) for record in records] 
        return response       

    async def select_presentation_parts(self, *, fk, presentation, media_type) -> List[PresentationMediaInDB]:
        medium = await self.__select_many(query=select_material_parts_query(fk=fk, presentation=presentation, media_type=media_type))
        if not medium:
            return []

        response = [PresentationMediaInDB(**r) for r in medium]
        return response

    async def select_all_presentation_parts(self, presentation: Union['theory', 'practice'], media_type: Union['image', 'audio']) -> List[AudioImagesAllModel]:
        """
        Returns list of order, keys for all presentation (theory | practice) parts (images| audio) in database
        """
        records = await self.__select_many(query=select_all_material_part_keys_query(presentation=presentation, media_type=media_type))

        response = [AudioImagesAllModel(**record) for record in records] 
        return response     

    # users
    async def select_user_available_grades(self, *, user_id: int) -> List[UserAvailableGrades]:
        records = await self.__select_many(query=select_all_user_available_grades_query(user_id=user_id))

        return [UserAvailableGrades(**record) for record in records]


    async def select_user_available_subjects(self, *, user_id: int) -> List[UserAvailableSubjects]:
        records = await self.__select_many(query=select_all_user_available_subjects_query(user_id=user_id))

        return [UserAvailableSubjects(**record) for record in records]


    # subscriptions
    # plans
    async def select_all_grade_subscription_plans(self) -> List[AvailableGradeSubscriptionPlans]:
        records = await self.__select_many(query=get_available_grade_plans_query())

        return [AvailableGradeSubscriptionPlans(**record) for record in records]

    async def select_all_subject_subscription_plans(self) -> List[AvailableSubjectSubscriptionPlans]:
        records = await self.__select_many(query=get_available_subject_plans_query())

        return [AvailableGradeSubscriptionPlans(**record) for record in records]


    # offers
    async def select_all_grade_subscription_offers(self) -> List[AvailableGradeSubscriptionOffers]:
        records = await self.__select_many(query=get_available_grade_offers_query())
        
        return [AvailableGradeSubscriptionOffers(**record) for record in records]
        
    async def select_all_subject_subscription_offers(self) -> List[AvailableSubjectSubscriptionOffers]:
        records = await self.__select_many(query=get_available_subject_offers_query())

        return [AvailableSubjectSubscriptionOffers(**record) for record in records]



    async def __select_many(self, *, query):
        try:
            response = await self.db.fetch_all(query=query)
        except Exception as e:
            logger.error("--- SELECT QUERY RAISED UNHANDLED ERROR ---") 
            logger.error(e)
            logger.error("--- SELECT QUERY RAISED UNHANDLED ERROR ---") 
            raise HTTPException(status_code=400, detail=f"Unhandled error raised trying to execute select query {query}. Error {e}")

        return response

    async def __select_one(self, *, query, raise_404=True):
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
