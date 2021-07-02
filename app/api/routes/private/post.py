from fastapi import APIRouter, HTTPException
from fastapi import Depends, Body
from starlette.status import HTTP_201_CREATED, HTTP_403_FORBIDDEN, HTTP_200_OK

from app.db.repositories.private.private import PrivateDBRepository
from app.cdn.repositories.private.private import PrivateYandexCDNRepository

from app.api.dependencies.database import get_db_repository
from app.api.dependencies.cdn import get_cdn_repository

from app.api.dependencies.auth import get_user_from_token, is_superuser, is_verified

# ###
# Request models
# ###
# material
from app.models.private import PresentationCreateModel
from app.models.private import BookPostModel, BookCreateModel
from app.models.private import VideoPostModelYT, VideoPostModelCDN, VideoCreateModel
from app.models.private import GamePostModel
from app.models.private import QuizPostModel, QuizCreateModel, QuizGetResultsModel
# structure
from app.models.private import GradePostModel, GradeCreateModel
from app.models.private import SubejctPostModel, SubjectCreateModel
from app.models.private import BranchPostModel, BranchCreateModel
from app.models.private import LecturePostModel, LectureCreateModel

# ### 
# Response models
# ###
# material
from app.models.private import PresentationInDB
from app.models.private import BookInDB
from app.models.private import VideoInDB
from app.models.private import GameInDB
from app.models.private import QuizQuestionInDB, QuizResults
# structure
from app.models.private import GradeInDB
from app.models.private import SubjectInDB
from app.models.private import BranchInDB
from app.models.private import LectureInDB
# subscriptions
from app.models.private import CreateGradeSubscriptionPlan
from app.models.private import CreateSubjectSubscriptionPlan

from app.models.user import UserInDB

router = APIRouter()

# ###
# content creation routes
# ###
@router.post("/practice", response_model=PresentationInDB, name="private:post-practice", status_code=HTTP_201_CREATED)
async def create_private_practice(
    presentation: PresentationCreateModel = Body(...),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    cdn_repo: PrivateYandexCDNRepository = Depends(get_cdn_repository(PrivateYandexCDNRepository)),
    is_superuser = Depends(is_superuser),
    is_verified = Depends(is_verified),
    ) -> PresentationInDB:
    if not is_superuser:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not superuser!")
    if not is_verified:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Email not verified!")

    # get images and audio formed data    
    (images, audio) = cdn_repo.form_presentation_insert_data(prefix=presentation.key, fk=presentation.fk)
    # insert into database
    response = await db_repo.insert_practice(presentation=presentation, images=images, audio=audio)

    return response

@router.post("/theory", response_model=PresentationInDB, name="private:post-theory", status_code=HTTP_201_CREATED)
async def create_private_theory(
    presentation: PresentationCreateModel = Body(...),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    cdn_repo: PrivateYandexCDNRepository = Depends(get_cdn_repository(PrivateYandexCDNRepository)),
    user: UserInDB = Depends(get_user_from_token),
    is_verified = Depends(is_verified),
    ) -> PresentationInDB:
    if not user.is_superuser:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not superuser!")
    if not is_verified:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Email not verified!")

    # get images and audio formed data    
    (images, audio) = cdn_repo.form_presentation_insert_data(prefix=presentation.key, fk=presentation.fk)
    # insert into database
    response = await db_repo.insert_theory(presentation=presentation, images=images, audio=audio)

    return response

@router.post("/book", response_model=BookInDB, name="private:post-book", status_code=HTTP_201_CREATED)
async def create_private_book(
    book: BookPostModel = Body(...),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    cdn_repo: PrivateYandexCDNRepository = Depends(get_cdn_repository(PrivateYandexCDNRepository)),
    user: UserInDB = Depends(get_user_from_token),
    is_verified = Depends(is_verified),
    ) -> BookInDB:
    if not user.is_superuser:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not superuser!")
    if not is_verified:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Email not verified!")

    (key, url) = cdn_repo.form_book_insert_data(prefix=book.key)
    book = BookCreateModel(key=key, url=url, name_ru=book.name_ru, description=book.description, fk=book.fk)
    response = await db_repo.insert_book(book=book)

    return response

@router.post("/video/youtube", response_model=VideoInDB, name="private:post-video-yt", status_code=HTTP_201_CREATED)
async def create_private_video(
    video: VideoPostModelYT = Body(...),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    user: UserInDB = Depends(get_user_from_token),
    is_verified = Depends(is_verified),
    ) -> VideoInDB:
    if not user.is_superuser:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not superuser!")
    if not is_verified:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Email not verified!")

    video = VideoCreateModel(fk=video.fk, url=video.url, name_ru=video.name_ru, description=video.description, key=None)
    response = await db_repo.insert_video(video=video, parse_link=True)

    return response

@router.post("/video/cdn", response_model=VideoInDB, name="private:post-video-cdn", status_code=HTTP_201_CREATED)
async def create_private_video(
    video: VideoPostModelCDN = Body(...),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    cdn_repo: PrivateYandexCDNRepository = Depends(get_cdn_repository(PrivateYandexCDNRepository)),
    user: UserInDB = Depends(get_user_from_token),
    is_verified = Depends(is_verified),
    ) -> VideoInDB:
    if not user.is_superuser:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not superuser!")
    if not is_verified:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Email not verified!")

    (key, url) = cdn_repo.form_video_insert_data(prefix=video.key)
    video = VideoCreateModel(key=key, url=url, name_ru=video.name_ru, description=video.description, fk=video.fk)
    response = await db_repo.insert_video(video=video)

    return response

@router.post("/game", response_model=GameInDB, name="private:post-game", status_code=HTTP_201_CREATED)
async def create_private_game(
    game: GamePostModel = Body(...),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    user: UserInDB = Depends(get_user_from_token),
    is_verified = Depends(is_verified),
    ) -> GameInDB:
    if not user.is_superuser:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not superuser!")
    if not is_verified:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Email not verified!")

    response = await db_repo.insert_game(game=game)

    return response

@router.post("/quiz", response_model=QuizQuestionInDB, name="private:post-quiz", status_code=HTTP_201_CREATED)
async def create_private_quiz(
    quiz: QuizPostModel = Body(...),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    cdn_repo: PrivateYandexCDNRepository = Depends(get_cdn_repository(PrivateYandexCDNRepository)),
    user: UserInDB = Depends(get_user_from_token),
    is_verified = Depends(is_verified),
    ) -> QuizQuestionInDB:
    if not user.is_superuser:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not superuser!")
    if not is_verified:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Email not verified!")

    if quiz.image_key:
        (key, url) = cdn_repo.form_quiz_insert_data(prefix=quiz.image_key)
        quiz = QuizCreateModel(image_url=url, answers=quiz.answers, image_key=key, lecture_id=quiz.lecture_id, order_number=quiz.order_number, question=quiz.question)
    else:
        quiz = QuizCreateModel(**quiz.dict(), image_url=None)
    response = await db_repo.insert_quiz_question(quiz_question=quiz)

    return response

@router.post("/quiz/results", response_model=QuizResults, name="private:get-quiz-results", status_code=HTTP_200_OK)
async def get_quiz_results(
    quiz_results: QuizGetResultsModel = Body(...),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    #user: UserInDB = Depends(get_user_from_token),
    #is_verified = Depends(is_verified),
    ) -> QuizResults:
    #if not is_verified:
    #  raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Email not verified!")

    response = await db_repo.check_quiz_results(quiz_results=quiz_results)

    return response


# ###
# structure creation routes
# ###
@router.post("/grade", response_model=GradeInDB, name="private:post-grade", status_code=HTTP_201_CREATED)
async def create_private_grade(
    grade: GradePostModel = Body(...),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    cdn_repo: PrivateYandexCDNRepository = Depends(get_cdn_repository(PrivateYandexCDNRepository)),
    user: UserInDB = Depends(get_user_from_token),
    is_verified = Depends(is_verified),
    ) -> GradeInDB:
    if not user.is_superuser:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not superuser!")
    if not is_verified:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Email not verified!")

    background = cdn_repo.get_background_url(key=grade.background_key, remove_extra=True)
    response  = await db_repo.insert_grade(grade=GradeCreateModel(name_en=grade.name_en , name_ru=grade.name_ru, background_key=grade.background_key, background=background, order_number=grade.order_number))

    return response


@router.post("/subject", response_model=SubjectInDB, name="private:post-subject", status_code=HTTP_201_CREATED)
async def create_private_subject(
    subject: SubejctPostModel = Body(...),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    cdn_repo: PrivateYandexCDNRepository = Depends(get_cdn_repository(PrivateYandexCDNRepository)),
    user: UserInDB = Depends(get_user_from_token),
    is_verified = Depends(is_verified),
    ) -> SubjectInDB:
    if not user.is_superuser:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not superuser!")
    if not is_verified:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Email not verified!")

    background = cdn_repo.get_background_url(key=subject.background_key, remove_extra=True)
    response  = await db_repo.insert_subject(subject=SubjectCreateModel(fk=subject.fk, name_en=subject.name_en , name_ru=subject.name_ru, background_key=subject.background_key, background=background, order_number=subject.order_number))

    return response

@router.post("/branch", response_model=BranchInDB, name="private:post-branch", status_code=HTTP_201_CREATED)
async def create_private_branch(
    branch: BranchPostModel = Body(...),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    cdn_repo: PrivateYandexCDNRepository = Depends(get_cdn_repository(PrivateYandexCDNRepository)),
    user: UserInDB = Depends(get_user_from_token),
    is_verified = Depends(is_verified),
    ) -> BranchInDB:
    if not user.is_superuser:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not superuser!")
    if not is_verified:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Email not verified!")

    background = cdn_repo.get_background_url(key=branch.background_key, remove_extra=True)    
    response  = await db_repo.insert_branch(branch=BranchCreateModel(fk=branch.fk, name_en=branch.name_en , name_ru=branch.name_ru, background_key=branch.background_key, background=background, order_number=branch.order_number))

    return response


@router.post("/lecture", response_model=LectureInDB, name="private:post-lecture", status_code=HTTP_201_CREATED)
async def create_private_lecture(
    lecture: LecturePostModel = Body(...),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    cdn_repo: PrivateYandexCDNRepository = Depends(get_cdn_repository(PrivateYandexCDNRepository)),
    user: UserInDB = Depends(get_user_from_token),
    is_verified = Depends(is_verified),
    ) -> LectureInDB:
    if not user.is_superuser:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not superuser!")
    if not is_verified:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Email not verified!")

    background = cdn_repo.get_background_url(key=lecture.background_key, remove_extra=True)    
    response  = await db_repo.insert_lecture(lecture=LectureCreateModel(fk=lecture.fk, name_en=lecture.name_en , name_ru=lecture.name_ru, description=lecture.description, background_key=lecture.background_key, background=background, order_number=lecture.order_number))

    return response

# Subscription plans
@router.post("/grade/subscription/plans")
async def create_grade_subscription_plan(
    grade_plan: CreateGradeSubscriptionPlan = Body(...),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    user: UserInDB = Depends(get_user_from_token),
    is_verified = Depends(is_verified),
    ) -> None:
    if not user.is_superuser:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not superuser!")
    if not is_verified:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Email not verified!")

    return await db_repo.insert_available_grade_plan(name=grade_plan.name, price=grade_plan.price, month_count=grade_plan.month_count)

@router.post("/subject/subscription/plans")
async def create_grade_subscription_plan(
    subject_plan: CreateSubjectSubscriptionPlan = Body(...),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    user: UserInDB = Depends(get_user_from_token),
    is_verified = Depends(is_verified),
    ) -> None:
    if not user.is_superuser:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not superuser!")
    if not is_verified:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Email not verified!")
    
    return await db_repo.insert_available_subject_plan(name=subject_plan.name, price=subject_plan.price, month_count=subject_plan.month_count)