from fastapi import APIRouter, Depends, Body, BackgroundTasks
from starlette.status import HTTP_200_OK

from app.db.repositories.private.private import PrivateDBRepository
from app.cdn.repositories.private.private import PrivateYandexCDNRepository
from app.db.repositories.parsers import parse_youtube_link

from app.api.dependencies.database import get_db_repository
from app.api.dependencies.cdn import get_cdn_repository

from app.api.dependencies.updating import update_sharing_links_function

from app.api.dependencies.auth import allowed_or_denied 


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

router = APIRouter()


# force update all links
@router.put("/update")
async def update_sharing_links(
    update = Depends(update_sharing_links_function),
    ) -> None:
    pass


@router.put("/grade", response_model=GradeInDB, name="private:put-grade", status_code=HTTP_200_OK)
async def update_private_grade(
    updated: UpdateStructureModel = Body(...),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    cdn_repo: PrivateYandexCDNRepository = Depends(get_cdn_repository(PrivateYandexCDNRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> GradeInDB:

    if updated.object_key:
        background_url = cdn_repo.get_background_url(object_key=updated.object_key)

    response = await db_repo.update_grade(updated=updated, background_url=background_url)
    return response

@router.put("/subject", response_model=SubjectInDB, name="private:put-subject", status_code=HTTP_200_OK)
async def update_private_subject( 
    updated: UpdateStructureModel = Body(...),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    cdn_repo: PrivateYandexCDNRepository = Depends(get_cdn_repository(PrivateYandexCDNRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> SubjectInDB:

    if updated.object_key:
        background_url = cdn_repo.get_background_url(object_key=updated.object_key)

    response = await db_repo.update_subject(updated=updated, background_url=background_url)
    return response

@router.put("/branch", response_model=BranchInDB, name="private:put-branch", status_code=HTTP_200_OK)
async def update_private_branch(
    updated: UpdateStructureModel = Body(...),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    cdn_repo: PrivateYandexCDNRepository = Depends(get_cdn_repository(PrivateYandexCDNRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> BranchInDB:

    if updated.object_key:
        background_url = cdn_repo.get_background_url(object_key=updated.object_key)

    response = await db_repo.update_branch(updated=updated, background_url=background_url)
    return response

@router.put("/lecture", response_model=LectureInDB, name="private:put-lecture", status_code=HTTP_200_OK)
async def update_private_lecture(
    updated: UpdateLectureModel = Body(...),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    cdn_repo: PrivateYandexCDNRepository = Depends(get_cdn_repository(PrivateYandexCDNRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> LectureInDB:

    if updated.object_key:
        background_url = cdn_repo.get_background_url(object_key=updated.object_key)

    response = await db_repo.update_lecture(updated=updated, background_url=background_url)
    return response

@router.put("/video", response_model=VideoInDB, name="private:put-video", status_code=HTTP_200_OK)
async def update_private_theory(
    updated: UpdateVideoModel = Body(...),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> VideoInDB:

    if updated.url:
        updated.url = parse_youtube_link(updated.url)

    response = await db_repo.update_video(updated=updated)
    return response

@router.put("/game", response_model=GameInDB, name="private:put-game", status_code=HTTP_200_OK)
async def update_private_game(
    updated: UpdateGameModel = Body(...),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> GameInDB:

    response = await db_repo.update_game(updated=updated)
    return response

@router.put("/book", response_model=BookInDB, name="private:put-book", status_code=HTTP_200_OK)
async def update_private_book(
    updated: UpdateBookModel = Body(...),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> BookInDB:

    response = await db_repo.update_book(updated=updated)
    return response

@router.put("/practice", response_model=PresentationMasterInDB, name="private:put-practice", status_code=HTTP_200_OK)
async def update_private_practice(
    updated: UpdatePresentationModel = Body(...),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> PresentationMasterInDB:

    response = await db_repo.update_presentation(updated=updated, presentation=ContentType.PRACTICE)
    return response

@router.put("/theory", response_model=PresentationMasterInDB, name="private:put-theory", status_code=HTTP_200_OK)
async def update_private_thoery(
    updated: UpdatePresentationModel = Body(...),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> PresentationMasterInDB:

    response = await db_repo.update_presentation(updated=updated, presentation=ContentType.THEORY)
    return response