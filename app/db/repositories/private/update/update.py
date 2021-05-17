from typing import Union
from fastapi import HTTPException

from app.db.repositories.private.update.queries import *

from app.db.repositories.base import BaseDBRepository

# import update models
from app.models.private import UpdateStructureModel
from app.models.private import UpdateLectureModel
from app.models.private import UpdateVideoModel
from app.models.private import UpdateGameModel
from app.models.private import UpdateBookModel
from app.models.private import UpdatePresentationModel

# import response models
from app.models.private import GradeInDB
from app.models.private import SubjectInDB
from app.models.private import BranchInDB
from app.models.private import LectureInDB
from app.models.private import VideoInDB
from app.models.private import GameInDB
from app.models.private import BookInDB
from app.models.private import PresentationMasterInDB


import logging

logger = logging.getLogger(__name__)

class PrivateDBUpdateRepository(BaseDBRepository):

    async def update_grade_links(self, *, grades) -> None:
        """
        Accepts dict with keys = 'background_key' and value = 'sharing link'
        Updates table grade by keys
        """
        keys = list(grades.keys())
        links = list(grades.values())
        await self.__update(query=update_grade_links_query(keys=keys, links=links))

    async def update_subject_links(self, *, subjects) -> None:
        """
        Accepts dict with keys = 'background_key' and value = 'sharing link'
        Updates table subject by keys
        """
        keys = list(subjects.keys())
        links = list(subjects.values())
        await self.__update(query=update_subject_links_query(keys=keys, links=links))

    async def update_branch_links(self, *, branches) -> None:
        """
        Accepts dict with keys = 'background_key' and value = 'sharing link'
        Updates table branch by keys
        """
        keys = list(branches.keys())
        links = list(branches.values())
        await self.__update(query=update_branch_links_query(keys=keys, links=links))

    async def update_lecture_links(self, *, lectures) -> None:
        """
        Accepts dict with keys = 'background_key' and value = 'sharing link'
        Updates table lecture by keys
        """
        keys = list(lectures.keys())
        links = list(lectures.values())
        await self.__update(query=update_lecture_links_query(keys=keys, links=links))


    async def update_book_links(self, *, book) -> None:
        """
        Accepts dict with keys = 'background_key' and value = 'sharing link'
        Updates table book by keys
        """
        keys = list(book.keys())
        links = list(book.values())
        await self.__update(query=update_book_links_query(keys=keys, links=links))

    # presentation prats
    async def update_presentation_part_links(self, *, prats, presentation: Union['theory', 'practice'], media_type: Union['image', 'audio']) -> None:
        """
        Accepts dict with keys = 'background_key' and value = 'sharing link'
        Updates table (theory | practice)_(image | audio) by keys
        """
        keys = list(prats.keys())
        links = list(prats.values())
        await self.__update(query=update_presentation_part_links_query(keys=keys, links=links, presentation=presentation, media_type=media_type))



    # ###
    # Update data
    # ###

    async def update_grade(self, *, updated: UpdateStructureModel, background_url: str = None) -> GradeInDB:
        """
        Accepts updated - updated model for structure
        background_url - if background_key is updated, background url is to be passed
        else leave it None
        """
        response = await self.__update(query=update_grade_query(id=updated.id, name_ru=updated.name_ru, background_url=background_url, background_key=updated.background_key))
        if not response:
            raise HTTPException(status_code=404, detail=f"Grade not updated, nothing found for give id {updated.id}")
        return GradeInDB(**response)


    async def update_subject(self, *, updated: UpdateStructureModel, background_url: str = None) -> SubjectInDB:
        """
        Accepts updated - updated model for structure
        background_url - if background_key is updated, background url is to be passed
        else leave it None
        """
        response = await self.__update(query=update_subject_query(id=updated.id, name_ru=updated.name_ru, background_url=background_url, background_key=updated.background_key))
        if not response:
            raise HTTPException(status_code=404, detail=f"Subject not updated, nothing found for give id {updated.id}")
        return SubjectInDB(**response)


    async def update_branch(self, *, updated: UpdateStructureModel, background_url: str = None) -> BranchInDB:
        """
        Accepts updated - updated model for structure
        background_url - if background_key is updated, background url is to be passed
        else leave it None
        """
        response = await self.__update(query=update_branch_query(id=updated.id, name_ru=updated.name_ru, background_url=background_url, background_key=updated.background_key))
        if not response:
            raise HTTPException(status_code=404, detail=f"Branch not updated, nothing found for give id {updated.id}")
        return BranchInDB(**response)


    async def update_lecture(self, *, updated: UpdateLectureModel, background_url: str = None) -> LectureInDB:
        """
        Accepts updated - updated model for lecture
        background_url - if background_key is updated, background url is to be passed
        else leave it None
        """
        response = await self.__update(query=update_lecture_query(id=updated.id, name_ru=updated.name_ru, description=updated.description, background_url=background_url, background_key=updated.background_key))
        if not response:
            raise HTTPException(status_code=404, detail=f"Lecture not updated, nothing found for give id {updated.id}")
        return LectureInDB(**response)



    async def update_video(self, *, updated: UpdateVideoModel) -> VideoInDB:
        """
        Accepts updated - updated model for video
        """
        response = await self.__update(query=update_video_query(id=updated.id, name_ru=updated.name_ru, description=updated.description, url=updated.url))
        if not response:
            raise HTTPException(status_code=404, detail=f"Video not updated, nothing found for give id {updated.id}")
        return VideoInDB(**response)

    
    async def update_game(self, *, updated: UpdateGameModel) -> GameInDB:
        """
        Accepts updated - updated model for video
        """
        response = await self.__update(query=update_game_query(id=updated.id, name_ru=updated.name_ru, description=updated.description, url=updated.url))
        if not response:
            raise HTTPException(status_code=404, detail=f"Game not updated, nothing found for give id {updated.id}")
        return GameInDB(**response)

    
    async def update_book(self, *, updated: UpdateBookModel) -> BookInDB:
        response = await self.__update(query=update_book_query(id=updated.id, description=updated.description, name_ru=updated.name_ru))
        if not response:
            raise HTTPException(status_code=404, detail="Nothing updated!")
        return BookInDB(**response)

    async def update_presentation(self, *, updated: UpdatePresentationModel, presentation: Union['practice', 'theory']):
        response = await self.__update(query=update_presentation_query(id=updated.id, description=updated.description, name_ru=updated.name_ru ,presentation=presentation))
        if not response:
            raise HTTPException(status_code=404, detail="Nothing updated!")
        return PresentationMasterInDB(id=response['id'], description=response['description'], name_ru=response['name_ru'])

    async def __update(self, *, query) -> None:
        try:
            updated = await self.db.fetch_one(query=query)
        except Exception as e:
            logger.error("--- ERROR TRYING TO UPDATE ---")
            logger.error(e)
            logger.error("--- ERROR TRYING TO UPDATE ---")
            raise HTTPException(status_code=400, detail=f"Error raised trying to update table. Query: {query}. Exited with {e}")

        return updated