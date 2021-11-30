from fastapi import APIRouter
from fastapi import Depends
from starlette.status import HTTP_200_OK

from app.db.repositories.public.public import PublicDBRepository
from app.cdn.repositories.public.public import PublicYandexCDNRepository

from app.api.dependencies.database import get_db_repository
from app.api.dependencies.cdn import get_cdn_repository

from app.api.dependencies.auth import allowed_or_denied

from app.models.user import UserInDB

router = APIRouter()

@router.delete("/theory", response_model=None, name="public:delete-theory", status_code=HTTP_200_OK)
async def delete_theory(
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    cdn_repo: PublicYandexCDNRepository = Depends(get_cdn_repository(PublicYandexCDNRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> None:

    deleted_key = await db_repo.delete_theory()
    if deleted_key:
        cdn_repo.delete_folder(folder=deleted_key)

    return None

@router.delete("/practice", response_model=None, name="public:delete-practice", status_code=HTTP_200_OK)
async def delete_practice(
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    cdn_repo: PublicYandexCDNRepository = Depends(get_cdn_repository(PublicYandexCDNRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> None:

    deleted_key = await db_repo.delete_practice()
    if deleted_key:
        cdn_repo.delete_folder(folder=deleted_key)

    return None

@router.delete("/book", response_model=None, name="public:delete-book", status_code=HTTP_200_OK)
async def delete_book(
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    cdn_repo: PublicYandexCDNRepository = Depends(get_cdn_repository(PublicYandexCDNRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> None:

    deleted_key = await db_repo.delete_book()
    if deleted_key:
        cdn_repo.delete_folder_by_inner_key(inner_key=deleted_key)

    return None


@router.delete("/video", response_model=None, name="public:delete-video", status_code=HTTP_200_OK)
async def delete_video(
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    cdn_repo: PublicYandexCDNRepository = Depends(get_cdn_repository(PublicYandexCDNRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> None:
    
    deleted_key = await db_repo.delete_video()
    if deleted_key:
        cdn_repo.delete_folder_by_inner_key(inner_key=deleted_key)

    return None

@router.delete("/intro/video", response_model=None, name="public:delete-intro-video", status_code=HTTP_200_OK)
async def delete_intro_video(
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    cdn_repo: PublicYandexCDNRepository = Depends(get_cdn_repository(PublicYandexCDNRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> None:
    
    deleted_key = await db_repo.delete_intro_video()
    if deleted_key:
        cdn_repo.delete_folder_by_inner_key(inner_key=deleted_key)

    return None

@router.delete("/quiz", response_model=None, name="public:delete-quiz", status_code=HTTP_200_OK)
async def delete_quiz(
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    cdn_repo: PublicYandexCDNRepository = Depends(get_cdn_repository(PublicYandexCDNRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> None:

    deleted_keys = await db_repo.delete_quiz()
    if deleted_keys:
        """We have a inconsistency here and in delete_quiz_question function. 
    
        In delete_quiz_question we are deleting folder containing object key is refering to,
        here we are deleting only the object.
        """
        cdn_repo.delete_keys(list_of_keys=deleted_keys)

    return None

@router.delete("/quiz/question", response_model=None, name="public:delete-quiz", status_code=HTTP_200_OK)
async def delete_quiz_question(
    id: int,
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    cdn_repo: PublicYandexCDNRepository = Depends(get_cdn_repository(PublicYandexCDNRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> None:

    deleted_key = await db_repo.delete_quiz_question(id=id)
    if deleted_key:
        """We have a inconsistency here and in delete_quiz function. 
    
        In delete_quiz we are deleting only the object that key is refering to,
        here we are deleting folder containing that object.
        """
        cdn_repo.delete_folder_by_inner_key(inner_key=deleted_key)

    return None


@router.delete("/game", response_model=None, name="public:delete-game", status_code=HTTP_200_OK)
async def delete_game(
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    cdn_repo: PublicYandexCDNRepository = Depends(get_cdn_repository(PublicYandexCDNRepository)),
    allowed: bool = Depends(allowed_or_denied),   
    ) -> None:

    deleted_key = await db_repo.delete_game()
    if deleted_key:
        cdn_repo.delete_folder_by_inner_key(inner_key=deleted_key)
    
    return None

@router.delete("/about_us", response_model=None, name="public:delete-about_us", status_code=HTTP_200_OK)
async def delete_about_us(
    order_number: int,
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> None:

    await db_repo.delete_about_us(order_number=order_number)
    return None

@router.delete("/faq", response_model=None, name="public:delete-faq", status_code=HTTP_200_OK)
async def delete_faq(
    id: int,
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> None:

    await db_repo.delete_faq(id=id)
    return None

@router.delete("/instructions", response_model=None, name="public:delete-instructions", status_code=HTTP_200_OK)
async def delete_instruction(
    order_number: int,
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> None:

    await db_repo.delete_instruction(order_number=order_number)
    return None

@router.delete("/review", response_model=None, name="public:delete-review", status_code=HTTP_200_OK)
async def delete_review(
    id: int,
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> None:

    await db_repo.delete_review(id=id)
    return None

@router.delete("/title/main", response_model=None, name="public:delete-main-title", status_code=HTTP_200_OK)
async def delete_main_title(
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> None:

    await db_repo.delete_main_title()
    return None

@router.delete("/title/example", response_model=None, name="public:delete-example-title", status_code=HTTP_200_OK)
async def delete_example_title(
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> None:

    await db_repo.delete_example_title()
    return None

@router.delete("/title/subscriptions", response_model=None, name="public:delete-subscriptions-title", status_code=HTTP_200_OK)
async def delete_subscriptions_title(
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> None:

    await db_repo.delete_subscriptions_title()
    return None

@router.delete("/title/questions", response_model=None, name="public:delete-questions-title", status_code=HTTP_200_OK)
async def delete_questions_title(
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> None:

    await db_repo.delete_questions_title()
    return None

@router.delete("/title/questions/sub", response_model=None, name="public:delete-questions-sub", status_code=HTTP_200_OK)
async def delete_questions_sub_title(
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> None:

    await db_repo.delete_questions_sub_title()
    return None
