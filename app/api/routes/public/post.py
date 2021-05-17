from fastapi import APIRouter, HTTPException
from fastapi import Depends, Body
from starlette.status import HTTP_201_CREATED

from app.db.repositories.public.public import PublicDBRepository
from app.cdn.repositories.public.public import PublicYandexCDNRepository

from app.api.dependencies.database import get_db_repository
from app.api.dependencies.cdn import get_cdn_repository
from app.api.dependencies.auth import get_user_from_token, is_superuser, is_verified

# post models
from app.models.public import PresentationPostModel
from app.models.public import BookPostModel
from app.models.public import VideoPostModelYT
from app.models.public import VideoPostModelCDN
from app.models.public import GamePostModel
from app.models.public import AboutUsPostModel
from app.models.public import FAQPostModel
from app.models.public import InstructionPostModel

# create models 
from app.models.public import PresentationCreateModel
from app.models.public import BookCreateModel
from app.models.public import VideoCreateModel
from app.models.public import GameCreateModel

# response models
from app.models.public import PresentationInDB
from app.models.public import BookInDB
from app.models.public import VideoInDB
from app.models.public import GameInDB

from app.models.public import AboutUsInDB
from app.models.public import FAQInDB
from app.models.public import InstructionInDB

from app.models.user import UserInDB

router = APIRouter()
# ###
# content creation routes
# ###
@router.post("/practice", response_model=PresentationInDB, name="public:post-practice", status_code=HTTP_201_CREATED)
async def create_public_practice(
    presentation: PresentationCreateModel = Body(...),
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    cdn_repo: PublicYandexCDNRepository = Depends(get_cdn_repository(PublicYandexCDNRepository)),
    user: UserInDB = Depends(get_user_from_token),
    is_superuser = Depends(is_superuser),
    is_verified = Depends(is_verified),
    ) -> PresentationInDB:
    if not user.is_superuser:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not superuser!")
    if not is_verified:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Email not verified!")

    # get images and audio formed data    
    (images, audio) = cdn_repo.form_presentation_insert_data(prefix=presentation.key)
    # insert into database
    response = await db_repo.insert_practice(presentation=presentation, images=images, audio=audio)

    return response

@router.post("/theory", response_model=PresentationInDB, name="public:post-theory", status_code=HTTP_201_CREATED)
async def create_public_theory(
    presentation: PresentationCreateModel = Body(...),
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    cdn_repo: PublicYandexCDNRepository = Depends(get_cdn_repository(PublicYandexCDNRepository)),
    user: UserInDB = Depends(get_user_from_token),
    is_superuser = Depends(is_superuser),
    is_verified = Depends(is_verified),
    ) -> PresentationInDB:
    if not user.is_superuser:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not superuser!")
    if not is_verified:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Email not verified!")

    # get images and audio formed data    
    (images, audio) = cdn_repo.form_presentation_insert_data(prefix=presentation.key)
    # insert into database
    response = await db_repo.insert_theory(presentation=presentation, images=images, audio=audio)

    return response

@router.post("/book", response_model=BookInDB, name="public:post-book", status_code=HTTP_201_CREATED)
async def create_public_book(
    book: BookPostModel = Body(...),
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    cdn_repo: PublicYandexCDNRepository = Depends(get_cdn_repository(PublicYandexCDNRepository)),
    user: UserInDB = Depends(get_user_from_token),
    is_superuser = Depends(is_superuser),
    is_verified = Depends(is_verified),
    ) -> BookInDB:
    if not user.is_superuser:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not superuser!")
    if not is_verified:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Email not verified!")

    (key, url) = cdn_repo.form_book_insert_data(prefix=book.key)
    book = BookCreateModel(key=key, url=url, name_ru=book.name_ru, description=book.description)
    response = await db_repo.insert_book(book=book)

    return response

@router.post("/video/youtube", response_model=VideoInDB, name="public:post-video-yt", status_code=HTTP_201_CREATED)
async def create_public_video(
    video: VideoPostModelYT = Body(...),
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    user: UserInDB = Depends(get_user_from_token),
    is_superuser = Depends(is_superuser),
    is_verified = Depends(is_verified),
    ) -> VideoInDB:
    if not user.is_superuser:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not superuser!")
    if not is_verified:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Email not verified!")

    video = VideoCreateModel(url=video.url, name_ru=video.name_ru, description=video.description, key=None)
    response = await db_repo.insert_video(video=video, parse_link=True)

    return response

@router.post("/video/cdn", response_model=VideoInDB, name="public:post-video-cdn", status_code=HTTP_201_CREATED)
async def create_public_video(
    video: VideoPostModelCDN = Body(...),
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    cdn_repo: PublicYandexCDNRepository = Depends(get_cdn_repository(PublicYandexCDNRepository)),
    user: UserInDB = Depends(get_user_from_token),
    is_superuser = Depends(is_superuser),
    is_verified = Depends(is_verified),
    ) -> VideoInDB:
    if not user.is_superuser:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not superuser!")
    if not is_verified:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Email not verified!")

    (key, url) = cdn_repo.form_video_insert_data(prefix=video.key)
    video = VideoCreateModel(key=key, url=url, name_ru=video.name_ru, description=video.description)
    response = await db_repo.insert_video(video=video)

    return response

@router.post("/game", response_model=GameInDB, name="public:post-game", status_code=HTTP_201_CREATED)
async def create_public_game(
    game: GamePostModel = Body(...),
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    user: UserInDB = Depends(get_user_from_token),
    is_superuser = Depends(is_superuser),
    is_verified = Depends(is_verified),
    ) -> GameInDB:
    if not user.is_superuser:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not superuser!")
    if not is_verified:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Email not verified!")

    response = await db_repo.insert_game(game=game)
    return response


# AboutUs, FAQ and Instructions

@router.post("/about_us", response_model=AboutUsInDB, name="public:post-about_us", status_code=HTTP_201_CREATED)
async def create_about_us(
    about_us: AboutUsPostModel = Body(...),
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    user: UserInDB = Depends(get_user_from_token),
    is_superuser = Depends(is_superuser),
    is_verified = Depends(is_verified),
    ) -> AboutUsInDB:
    if not user.is_superuser:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not superuser!")
    if not is_verified:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Email not verified!")

    response = await db_repo.insert_about_us(about_us=about_us)
    return response

@router.post("/instructions", response_model=InstructionInDB, name="public:post-instruction", status_code=HTTP_201_CREATED)
async def create_instructions(
    instruction: InstructionPostModel = Body(...),
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    user: UserInDB = Depends(get_user_from_token),
    is_superuser = Depends(is_superuser),
    is_verified = Depends(is_verified),
    ) -> InstructionInDB:
    if not user.is_superuser:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not superuser!")
    if not is_verified:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Email not verified!")

    response = await db_repo.insert_instruction(instruction=instruction)
    return response

@router.post("/faq", response_model=FAQInDB, name="public:post-faq", status_code=HTTP_201_CREATED)
async def create_faq(
    faq: FAQPostModel = Body(...),
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    user: UserInDB = Depends(get_user_from_token),
    is_superuser = Depends(is_superuser),
    is_verified = Depends(is_verified),
    ) -> FAQInDB:
    if not user.is_superuser:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not superuser!")
    if not is_verified:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Email not verified!")

    response = await db_repo.insert_faq(faq=faq)
    return response