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

from app.db.repositories.types import ContentType

import logging

logger = logging.getLogger(__name__)

class PrivateDBUpdateRepository(BaseDBRepository):
    # LINK UPDATING FUNCTIONS
    async def update_grade_links(self, *, grades) -> None:
        """Updates private grade presigned urls by keys.
        
        Keyword arguemts;
        grades -- dictionary with:
            key   -- objecy_key
            value -- presigned url 
        """
        keys = list(grades.keys())
        links = list(grades.values())
        await self._execute_one(query=update_grade_links_query(keys=keys, links=links))

    async def update_subject_links(self, *, subjects) -> None:
        """Updates private subject presigned urls by keys.
        
        Keyword arguemts;
        subjects -- dictionary with:
            key   -- objecy_key
            value -- presigned url 
        """
        keys = list(subjects.keys())
        links = list(subjects.values())
        await self._execute_one(query=update_subject_links_query(keys=keys, links=links))

    async def update_branch_links(self, *, branches) -> None:
        """Updates private branch presigned urls by keys.
        
        Keyword arguemts;
        branches -- dictionary with:
            key   -- objecy_key
            value -- presigned url 
        """
        keys = list(branches.keys())
        links = list(branches.values())
        await self._execute_one(query=update_branch_links_query(keys=keys, links=links))

    async def update_lecture_links(self, *, lectures) -> None:
        """Updates private lecture presigned urls by keys.
        
        Keyword arguemts;
        lectures -- dictionary with:
            key   -- objecy_key
            value -- presigned url 
        """
        keys = list(lectures.keys())
        links = list(lectures.values())
        await self._execute_one(query=update_lecture_links_query(keys=keys, links=links))


    async def update_book_links(self, *, book) -> None:
        """Updates private book presigned urls by keys.
        
        Keyword arguemts;
        book -- dictionary with:
            key   -- objecy_key
            value -- presigned url 
        """
        keys = list(book.keys())
        links = list(book.values())
        await self._execute_one(query=update_book_links_query(keys=keys, links=links))

    async def update_video_links(self, *, video) -> None:
        """Updates private video presigned urls by keys.
        
        Keyword arguemts;
        video -- dictionary with:
            key   -- objecy_key
            value -- presigned url 
        """
        keys = list(video.keys())
        links = list(video.values())
        await self._execute_one(query=update_video_links_query(keys=keys, links=links))

    async def update_game_links(self, *, game) -> None:
        """Updates private game presigned urls by keys.
        
        Keyword arguemts;
        game -- dictionary with:
            key   -- objecy_key
            value -- presigned url 
        """
        keys = list(game.keys())
        links = list(game.values())
        await self._execute_one(query=update_game_links_query(keys=keys, links=links))

    async def update_quiz_links(self, *, quiz) -> None:
        """Updates private quiz presigned urls by keys.
        
        Keyword arguemts;
        quiz -- dictionary with:
            key   -- objecy_key
            value -- presigned url 
        """
        keys = list(quiz.keys())
        links = list(quiz.values())
        await self._execute_one(query=update_quiz_links_query(keys=keys, links=links))

    async def update_presentation_part_links(self, *, prats, presentation: ContentType, media_type: ContentType) -> None:
        """Updates private presentation presigned urls by keys.
        
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
    async def update_grade(self, *, updated: UpdateStructureModel, background_url: str = None) -> GradeInDB:
        """Updates private grade."""
        response = await self._fetch_one(query=update_grade_query(**updated.dict(), background_url=background_url))
        if not response:
            raise HTTPException(status_code=404, detail=f"Grade not updated, nothing found for given id {updated.id}")
        return GradeInDB(**response)

    async def update_subject(self, *, updated: UpdateStructureModel, background_url: str = None) -> SubjectInDB:
        """Updates private subject."""
        response = await self._fetch_one(query=update_subject_query(**updated.dict(), background_url=background_url))
        if not response:
            raise HTTPException(status_code=404, detail=f"Subject not updated, nothing found for given id {updated.id}")
        return SubjectInDB(**response)

    async def update_branch(self, *, updated: UpdateStructureModel, background_url: str = None) -> BranchInDB:
        """Updates private branch"""
        response = await self._fetch_one(query=update_branch_query(**updated.dict(), background_url=background_url))
        if not response:
            raise HTTPException(status_code=404, detail=f"Branch not updated, nothing found for given id {updated.id}")
        return BranchInDB(**response)

    async def update_lecture(self, *, updated: UpdateLectureModel, background_url: str = None) -> LectureInDB:
        """Updates private lecture."""
        response = await self._fetch_one(query=update_lecture_query(**updated.dict(), background_url=background_url))
        if not response:
            raise HTTPException(status_code=404, detail=f"Lecture not updated, nothing found for given id {updated.id}")
        return LectureInDB(**response)


    async def update_video(self, *, updated: UpdateVideoModel) -> VideoInDB:
        """Updates private video"""
        response = await self._fetch_one(query=update_video_query(**updated.dict()))
        if not response:
            raise HTTPException(status_code=404, detail=f"Video not updated, nothing found for given id {updated.id}")
        return VideoInDB(**response)
    
    async def update_game(self, *, updated: UpdateGameModel) -> GameInDB:
        """Updates private game"""
        response = await self._fetch_one(query=update_game_query(**updated.dict()))
        if not response:
            raise HTTPException(status_code=404, detail=f"Game not updated, nothing found for given id {updated.id}")
        return GameInDB(**response)

    async def update_book(self, *, updated: UpdateBookModel) -> BookInDB:
        """Updates private book"""
        response = await self._fetch_one(query=update_book_query(**updated.dict()))
        if not response:
            raise HTTPException(status_code=404, detail=f"Book not updated, nothing found for given id {updated.id}")
        return BookInDB(**response)

    async def update_presentation(self, *, updated: UpdatePresentationModel, presentation: ContentType) -> PresentationMasterInDB:
        """Updates private presentation.
        
        Keyword arguments:
        updated      -- updated presentation
        presentation -- ContentType determening table of presentation we want to update. 
        """
        response = await self._fetch_one(query=update_presentation_query(**updated.dict(), presentation=presentation.value))
        if not response:
            raise HTTPException(status_code=404, detail="Presentation not updated!")
        return PresentationMasterInDB(**response)
