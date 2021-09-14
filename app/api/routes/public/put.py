from fastapi import APIRouter
from fastapi import Depends, Body
from starlette.status import HTTP_200_OK

from app.db.repositories.public.public import PublicDBRepository

from app.api.dependencies.database import get_db_repository

from app.db.repositories.parsers import parse_youtube_link

from app.api.dependencies.auth import allowed_or_denied

# import update models
from app.models.public import UpdateVideoModel
from app.models.public import UpdateGameModel
from app.models.public import UpdateBookModel
from app.models.public import UpdatePresentationModel
from app.models.public import UpdateAboutUsModel
from app.models.public import UpdateFAQModel
from app.models.public import UpdateInstructionModel

# import response models
from app.models.public import VideoInDB
from app.models.public import GameInDB
from app.models.public import BookInDB
from app.models.public import PresentationMasterInDB
from app.models.public import AboutUsInDB
from app.models.public import FAQInDB
from app.models.public import InstructionInDB

from app.db.repositories.types import ContentType

from app.models.user import UserInDB

router = APIRouter()


@router.put("/video", response_model=VideoInDB, name="public:update-video", status_code=HTTP_200_OK)
async def update_video(
    updated: UpdateVideoModel = Body(...),
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> VideoInDB:

    response = await db_repo.update_video(updated=updated)
    return response

@router.put("/game", response_model=GameInDB, name="public:update-game", status_code=HTTP_200_OK)
async def update_game(
    game: UpdateGameModel = Body(...),
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> GameInDB:

    response = await db_repo.update_game(updated=game)
    return response

""" NEW """

@router.put("/book", response_model=BookInDB, name="public:update-book", status_code=HTTP_200_OK)
async def update_public_book(
    updated: UpdateBookModel = Body(...),
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> BookInDB:

    response = await db_repo.update_book(updated=updated)
    return response

@router.put("/practice", response_model=PresentationMasterInDB, name="public:update-practice", status_code=HTTP_200_OK)
async def update_public_practice(
    updated: UpdatePresentationModel = Body(...),
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> PresentationMasterInDB:

    response = await db_repo.update_presentation(updated=updated, presentation=ContentType.PRACTICE)
    return response

@router.put("/theory", response_model=PresentationMasterInDB, name="public:update-theory", status_code=HTTP_200_OK)
async def update_public_practice(
    updated: UpdatePresentationModel = Body(...),
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> PresentationMasterInDB:

    response = await db_repo.update_presentation(updated=updated, presentation=ContentType.THEORY)
    return response

""" END NEW """


@router.put("/about_us", response_model=AboutUsInDB, name="public:update-about_us", status_code=HTTP_200_OK)
async def update_about_us(
    about_us: UpdateAboutUsModel = Body(...),
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> AboutUsInDB:

    response = await db_repo.update_about_us(updated=about_us)
    return response

@router.put("/faq", response_model=FAQInDB, name="public:update-faq", status_code=HTTP_200_OK)
async def update_faq(
    faq: UpdateFAQModel = Body(...),
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> FAQInDB:

    response = await db_repo.update_faq(updated=faq)
    return response

@router.put("/instructions", response_model=InstructionInDB, name="public:update-instruction", status_code=HTTP_200_OK)
async def update_instruction(
    instruction: UpdateInstructionModel = Body(...),
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> InstructionInDB:

    response = await db_repo.update_instruction(updated=instruction)
    return response