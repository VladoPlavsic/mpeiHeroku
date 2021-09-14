from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK

from app.db.repositories.private.private import PrivateDBRepository
from app.cdn.repositories.private.private import PrivateYandexCDNRepository

from app.api.dependencies.database import get_db_repository
from app.api.dependencies.cdn import get_cdn_repository

from app.api.dependencies.auth import allowed_or_denied

router = APIRouter()

@router.delete('/grade', response_model=None, name="private:delete-grade", status_code=HTTP_200_OK)
async def delete_private_grade(
    id: int,
    cdn_repo: PrivateYandexCDNRepository = Depends(get_cdn_repository(PrivateYandexCDNRepository)),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> None:

    deleted_key = await db_repo.delete_grade(id=id)
    if deleted_key:
        cdn_repo.delete_folder_by_inner_key(inner_key=deleted_key)

    return None

@router.delete('/subject', response_model=None, name="private:delete-subject", status_code=HTTP_200_OK)
async def delete_private_subject(
    id: int,
    cdn_repo: PrivateYandexCDNRepository = Depends(get_cdn_repository(PrivateYandexCDNRepository)),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> None:

    deleted_key = await db_repo.delete_subject(id=id)
    if deleted_key:
        cdn_repo.delete_folder_by_inner_key(inner_key=deleted_key)

    return None

@router.delete('/branch', response_model=None, name="private:delete-branch", status_code=HTTP_200_OK)
async def delete_private_branch(
    id: int,
    cdn_repo: PrivateYandexCDNRepository = Depends(get_cdn_repository(PrivateYandexCDNRepository)),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> None:

    deleted_key = await db_repo.delete_branch(id=id)
    if deleted_key:
        cdn_repo.delete_folder_by_inner_key(inner_key=deleted_key)

    return None

@router.delete('/lecture', response_model=None, name="private:delete-lecture", status_code=HTTP_200_OK)
async def delete_private_lecture(
    id: int,
    cdn_repo: PrivateYandexCDNRepository = Depends(get_cdn_repository(PrivateYandexCDNRepository)),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> None:

    deleted_key = await db_repo.delete_lecture(id=id)
    if deleted_key:
        cdn_repo.delete_folder_by_inner_key(inner_key=deleted_key)

    return None

@router.delete('/theory', response_model=None, name="private:delete-theory", status_code=HTTP_200_OK)
async def delete_private_theory(
    id: int,
    cdn_repo: PrivateYandexCDNRepository = Depends(get_cdn_repository(PrivateYandexCDNRepository)),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> None:

    deleted_key = await db_repo.delete_theory(id=id)
    if deleted_key:
        cdn_repo.delete_folder(folder=deleted_key)

    return None

@router.delete('/practice', response_model=None, name="private:delete-practice", status_code=HTTP_200_OK)
async def delete_private_practice(
    id: int,
    cdn_repo: PrivateYandexCDNRepository = Depends(get_cdn_repository(PrivateYandexCDNRepository)),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> None:

    deleted_key = await db_repo.delete_practice(id=id)
    if deleted_key:
        cdn_repo.delete_folder(folder=deleted_key)

    return None

@router.delete('/book', response_model=None, name="private:delete-book", status_code=HTTP_200_OK)
async def delete_private_book(
    id: int,
    cdn_repo: PrivateYandexCDNRepository = Depends(get_cdn_repository(PrivateYandexCDNRepository)),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> None:

    deleted_key = await db_repo.delete_book(id=id)
    if deleted_key:
        cdn_repo.delete_folder_by_inner_key(inner_key=deleted_key)

    return None

@router.delete('/video', response_model=None, name="private:delete-video", status_code=HTTP_200_OK)
async def delete_private_video(
    id: int,
    cdn_repo: PrivateYandexCDNRepository = Depends(get_cdn_repository(PrivateYandexCDNRepository)),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> None:

    deleted_key = await db_repo.delete_video(id=id)
    if deleted_key:
        cdn_repo.delete_folder_by_inner_key(inner_key=deleted_key)

    return None

@router.delete("/quiz", response_model=None, name="private:delete-quiz", status_code=HTTP_200_OK)
async def delete_private_quiz(
    fk: int,
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    cdn_repo: PrivateYandexCDNRepository = Depends(get_cdn_repository(PrivateYandexCDNRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> None:

    deleted_keys = await db_repo.delete_quiz(fk=fk)
    if deleted_keys:
        """We have a inconsistency here and in delete_private_quiz_questions function. 
    
        In delete_private_quiz_questions we are deleting folder containing object key is refering to,
        here we are deleting only the object.
        """
        cdn_repo.delete_keys(list_of_keys=deleted_keys)

    return None

@router.delete("/quiz/question", response_model=None, name="private:delete-quiz", status_code=HTTP_200_OK)
async def delete_private_quiz_questions(
    id: int,
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    cdn_repo: PrivateYandexCDNRepository = Depends(get_cdn_repository(PrivateYandexCDNRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> None:

    deleted_key = await db_repo.delete_quiz_question(id=id)
    if deleted_key:
        """We have a inconsistency here and in delete_private_quiz function. 
    
        In delete_private_quiz we are deleting only the object that key is refering to,
        here we are deleting folder containing that object.
        """
        cdn_repo.delete_folder_by_inner_key(inner_key=deleted_key)

    return None


@router.delete('/game', response_model=None, name="private:delete-game", status_code=HTTP_200_OK)
async def delete_private_game(
    id: int,
    cdn_repo: PrivateYandexCDNRepository = Depends(get_cdn_repository(PrivateYandexCDNRepository)),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> None:

    deleted_key = await db_repo.delete_game(id=id)
    if deleted_key:
        cdn_repo.delete_folder_by_inner_key(inner_key=deleted_key)

    return None


# Subscription plans
@router.delete("/grade/subscription/plans", response_model=None, name="private:delete-grade-subscription-plan", status_code=HTTP_200_OK)
async def delete_grade_subscription_plan(
    id: int,
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> None:

    return await db_repo.delete_grade_subscription_plan(id=id)

@router.delete("/subject/subscription/plans", response_model=None, name="private:delete-subject-subscription-plan", status_code=HTTP_200_OK)
async def delete_subject_subscription_plan(
    id: int,
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> None:

    return await db_repo.delete_subject_subscription_plan(id=id)
