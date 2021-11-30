from fastapi import APIRouter, HTTPException
from fastapi import Depends, Body
from starlette.status import HTTP_201_CREATED, HTTP_200_OK

from app.db.repositories.public.public import PublicDBRepository
from app.cdn.repositories.public.public import PublicYandexCDNRepository

from app.api.dependencies.database import get_db_repository
from app.api.dependencies.cdn import get_cdn_repository
from app.api.dependencies.auth import allowed_or_denied

# post models
from app.models.public import PresentationPostModel
from app.models.public import BookPostModel
from app.models.public import VideoPostModelYT
from app.models.public import VideoPostModelCDN
from app.models.public import IntroVideoPostModelYT
from app.models.public import IntroVideoPostModelCDN
from app.models.public import GamePostModel
from app.models.public import QuizPostModel, QuizGetResultsModel
from app.models.public import AboutUsPostModel
from app.models.public import FAQPostModel
from app.models.public import InstructionPostModel
from app.models.public import ReviewPostModel
from app.models.public import TitlesPostModel

# create models 
from app.models.public import PresentationCreateModel
from app.models.public import BookCreateModel
from app.models.public import VideoCreateModel
from app.models.public import IntroVideoCreateModel
from app.models.public import QuizCreateModel
from app.models.public import GameCreateModel
from app.models.public import ReviewCreateModel

# response models
from app.models.public import PresentationInDB
from app.models.public import BookInDB
from app.models.public import VideoInDB
from app.models.public import IntroVideoInDB
from app.models.public import GameInDB
from app.models.public import QuizQuestionInDB, QuizResults
from app.models.public import AboutUsInDB
from app.models.public import FAQInDB
from app.models.public import InstructionInDB
from app.models.public import ReviewInDB
from app.models.public import TitlesInDB

from app.cdn.types import DefaultFormats

router = APIRouter()
# ###
# content creation routes
# ###
@router.post("/practice", response_model=PresentationInDB, name="public:post-practice", status_code=HTTP_201_CREATED)
async def create_public_practice(
    presentation: PresentationCreateModel = Body(...),
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    cdn_repo: PublicYandexCDNRepository = Depends(get_cdn_repository(PublicYandexCDNRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> PresentationInDB:
    
    images = cdn_repo.format_presentation_content(folder=presentation.object_key, type_=DefaultFormats.IMAGES)
    audio = cdn_repo.format_presentation_content(folder=presentation.object_key, type_=DefaultFormats.AUDIO)

    response = await db_repo.insert_practice(presentation=presentation, images=images, audio=audio)

    return response

@router.post("/theory", response_model=PresentationInDB, name="public:post-theory", status_code=HTTP_201_CREATED)
async def create_public_theory(
    presentation: PresentationCreateModel = Body(...),
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    cdn_repo: PublicYandexCDNRepository = Depends(get_cdn_repository(PublicYandexCDNRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> PresentationInDB:

    images = cdn_repo.format_presentation_content(folder=presentation.object_key, type_=DefaultFormats.IMAGES)
    audio = cdn_repo.format_presentation_content(folder=presentation.object_key, type_=DefaultFormats.AUDIO)

    response = await db_repo.insert_theory(presentation=presentation, images=images, audio=audio)

    return response

@router.post("/book", response_model=BookInDB, name="public:post-book", status_code=HTTP_201_CREATED)
async def create_public_book(
    book: BookPostModel = Body(...),
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    cdn_repo: PublicYandexCDNRepository = Depends(get_cdn_repository(PublicYandexCDNRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> BookInDB:
    
    shared = cdn_repo.form_book_insert_data(folder=book.object_key)
    object_key = list(shared[0].keys())[0]
    url = shared[0][object_key]
    book.object_key = object_key
    book = BookCreateModel(**book.dict(), url=url)
    response = await db_repo.insert_book(book=book)

    return response

@router.post("/video/youtube", response_model=VideoInDB, name="public:post-video-yt", status_code=HTTP_201_CREATED)
async def create_public_video(
    video: VideoPostModelYT = Body(...),
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    cdn_repo: PublicYandexCDNRepository = Depends(get_cdn_repository(PublicYandexCDNRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> VideoInDB:

    # First delete video this way. The old way doesn't delete video from CDN !
    deleted_key = await db_repo.delete_video()
    if deleted_key:
        cdn_repo.delete_folder_by_inner_key(inner_key=deleted_key)

    video = VideoCreateModel(**video.dict(), object_key=None)
    response = await db_repo.insert_video(video=video, parse_link=True)

    return response

@router.post("/video/cdn", response_model=VideoInDB, name="public:post-video-cdn", status_code=HTTP_201_CREATED)
async def create_public_video(
    video: VideoPostModelCDN = Body(...),
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    cdn_repo: PublicYandexCDNRepository = Depends(get_cdn_repository(PublicYandexCDNRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> VideoInDB:

    deleted_key = await db_repo.delete_video()
    if deleted_key:
        cdn_repo.delete_folder_by_inner_key(inner_key=deleted_key)

    shared = cdn_repo.form_video_insert_data(folder=video.object_key)
    object_key = list(shared[0].keys())[0]
    url = shared[0][object_key]
    video.object_key = object_key
    video = VideoCreateModel(**video.dict(), url=url)
    response = await db_repo.insert_video(video=video)

    return response

@router.post("/intro/video/youtube", response_model=IntroVideoInDB, name="public:post-intro-video-yt", status_code=HTTP_201_CREATED)
async def create_public_video(
    video: IntroVideoPostModelYT = Body(...),
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    cdn_repo: PublicYandexCDNRepository = Depends(get_cdn_repository(PublicYandexCDNRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> IntroVideoInDB:

    deleted_key = await db_repo.delete_intro_video()
    print(deleted_key)
    if deleted_key:
        cdn_repo.delete_folder_by_inner_key(inner_key=deleted_key)

    video = IntroVideoCreateModel(**video.dict(), object_key=None)
    response = await db_repo.insert_intro_video(video=video, parse_link=True)

    return response

@router.post("/intro/video/cdn", response_model=IntroVideoInDB, name="public:post-intro-video-cdn", status_code=HTTP_201_CREATED)
async def create_public_video(
    video: IntroVideoPostModelCDN = Body(...),
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    cdn_repo: PublicYandexCDNRepository = Depends(get_cdn_repository(PublicYandexCDNRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> VideoInDB:

    deleted_key = await db_repo.delete_intro_video()
    if deleted_key:
        cdn_repo.delete_folder_by_inner_key(inner_key=deleted_key)

    shared = cdn_repo.form_video_insert_data(folder=video.object_key)
    object_key = list(shared[0].keys())[0]
    url = shared[0][object_key]
    video.object_key = object_key
    video = IntroVideoCreateModel(**video.dict(), url=url)
    response = await db_repo.insert_intro_video(video=video)

    return response

@router.post("/game", response_model=GameInDB, name="public:post-game", status_code=HTTP_201_CREATED)
async def create_public_game(
    game: GamePostModel = Body(...),
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    cdn_repo: PublicYandexCDNRepository = Depends(get_cdn_repository(PublicYandexCDNRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> GameInDB:

    shared = cdn_repo.form_game_insert_data(folder=game.object_key)
    object_key = list(shared[0].keys())[0]
    url = shared[0][object_key]
    game.object_key = object_key
    game = GameCreateModel(**game.dict(), url=url)
    response = await db_repo.insert_game(game=game)

    return response

@router.post("/quiz", response_model=QuizQuestionInDB, name="public:post-quiz", status_code=HTTP_201_CREATED)
async def create_private_quiz(
    quiz: QuizPostModel = Body(...),
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    cdn_repo: PublicYandexCDNRepository = Depends(get_cdn_repository(PublicYandexCDNRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> QuizQuestionInDB:

    if quiz.object_key:
        shared = cdn_repo.form_quiz_insert_data(folder=quiz.object_key)
        object_key = list(shared[0].keys())[0]
        url = shared[0][object_key]
        quiz.object_key = object_key
        quiz = QuizCreateModel(**quiz.dict(), image_url=url)
    else:
        quiz = QuizCreateModel(**quiz.dict(), image_url=None)
    response = await db_repo.insert_quiz_question(quiz_question=quiz)

    return response

@router.post("/quiz/results", response_model=QuizResults, name="private:get-quiz-results", status_code=HTTP_200_OK)
async def get_quiz_results(
    quiz_results: QuizGetResultsModel = Body(...),
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    ) -> QuizResults:

    response = await db_repo.check_quiz_results(quiz_results=quiz_results)

    return response

# AboutUs, FAQ and Instructions
@router.post("/about_us", response_model=AboutUsInDB, name="public:post-about_us", status_code=HTTP_201_CREATED)
async def create_about_us(
    about_us: AboutUsPostModel = Body(...),
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> AboutUsInDB:
    
    response = await db_repo.insert_about_us(about_us=about_us)
    return response

@router.post("/instructions", response_model=InstructionInDB, name="public:post-instruction", status_code=HTTP_201_CREATED)
async def create_instructions(
    instruction: InstructionPostModel = Body(...),
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> InstructionInDB:

    response = await db_repo.insert_instruction(instruction=instruction)
    return response

@router.post("/faq", response_model=FAQInDB, name="public:post-faq", status_code=HTTP_201_CREATED)
async def create_faq(
    faq: FAQPostModel = Body(...),
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> FAQInDB:

    response = await db_repo.insert_faq(faq=faq)
    return response

@router.post("/review", response_model=ReviewInDB, name="public:post-review", status_code=HTTP_201_CREATED)
async def create_review(
    review: ReviewPostModel = Body(...),
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    cdn_repo: PublicYandexCDNRepository = Depends(get_cdn_repository(PublicYandexCDNRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> ReviewInDB:
    
    shared = cdn_repo.get_sharing_link_from_object_key(object_key=review.object_key)
    review = ReviewCreateModel(**review.dict(), image_url=shared[review.object_key])
    response = await db_repo.insert_review(review=review)
    return response

@router.post("/titles", response_model=TitlesInDB, name="public:post-titles", status_code=HTTP_201_CREATED)
async def insert_titles(
    titles: TitlesPostModel = Body(...),
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> TitlesInDB:

    response = await db_repo.insert_title(titles=titles)
    return response
