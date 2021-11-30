from fastapi import APIRouter, HTTPException
from fastapi import Depends
from starlette.status import HTTP_200_OK

from app.db.repositories.public.public import PublicDBRepository
from app.cdn.repositories.public.public import PublicYandexCDNRepository

from app.api.dependencies.database import get_db_repository
from app.api.dependencies.cdn import get_cdn_repository


# response models
from app.models.public import MaterialResponse
from app.models.public import AboutUsAllResponse
from app.models.public import FaqAllResponse
from app.models.public import InstructionAllResponse
from app.models.public import IntroVideoAllResponse
from app.models.public import ReviewResponse
from app.models.public import TitlesResponseModel

router = APIRouter()

@router.get("/material", response_model=MaterialResponse, name="public:get-material", status_code=HTTP_200_OK)
async def get_public_material(
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    ) -> MaterialResponse:

    response = await db_repo.select_material()
    return MaterialResponse(material=response)

@router.get("/intro/video", response_model=IntroVideoAllResponse, name="public:get-intro-video", status_code=HTTP_200_OK)
async def get_intro_video(
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    ) -> IntroVideoAllResponse:

    response = await db_repo.select_intro_video()
    return IntroVideoAllResponse(intro=response)

@router.get("/about_us", response_model=AboutUsAllResponse, name="public:get-about_us", status_code=HTTP_200_OK)
async def get_about_us(
    public_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository))
    ) -> AboutUsAllResponse:

    response = await public_repo.select_about_us()
    return AboutUsAllResponse(about_us=response)

@router.get("/instructions", response_model=InstructionAllResponse, name="public:get-instructions", status_code=HTTP_200_OK)
async def get_instructions(
    public_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository))
    ) -> InstructionAllResponse:

    response = await public_repo.select_instructions()
    return InstructionAllResponse(instructions=response)

@router.get("/faq", response_model=FaqAllResponse, name="public:get-faq", status_code=HTTP_200_OK)
async def get_faq(
    limit: int = 0,
    offset: int = 0,
    public_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository))
    ) -> FaqAllResponse:

    if limit == 0:
        limit = None
    response = await public_repo.select_faq(limit=limit, offset=offset)

    return FaqAllResponse(faq=response)

@router.get("/review", response_model=ReviewResponse, name="public:get-reviews", status_code=HTTP_200_OK)
async def get_reviews(
    public_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository))
    ) -> ReviewResponse:

    response = await public_repo.select_reivew()
    return ReviewResponse(reviews=response)


@router.get("/titles", response_model=TitlesResponseModel, name="public:get-titles", status_code=HTTP_200_OK)
async def get_titles(
    public_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository))
    ) -> TitlesResponseModel:

    response = await public_repo.get_titles()
    return response

# TEMPORARY FOR KEEPING SERVER AWAKE (FREE HEROKU HOSING)
@router.get("/wake/")
async def wake_server() -> None:
    return None