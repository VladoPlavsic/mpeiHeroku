from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK

from app.db.repositories.private.private import PrivateDBRepository
from app.cdn.repositories.private.private import PrivateYandexCDNRepository

from app.api.dependencies.database import get_db_repository
from app.api.dependencies.cdn import get_cdn_repository

from app.api.dependencies.auth import get_user_from_token, is_superuser, is_verified

from app.models.user import UserInDB

router = APIRouter()

@router.delete('/grade', response_model=None, name="private:delete-grade", status_code=HTTP_200_OK)
async def delete_private_grade(
    id: int,
    cdn_repo: PrivateYandexCDNRepository = Depends(get_cdn_repository(PrivateYandexCDNRepository)),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    user: UserInDB = Depends(get_user_from_token),
    is_superuser = Depends(is_superuser),
    is_verified = Depends(is_verified),
    ) -> None:
    if not user.is_superuser:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not superuser!")
    if not is_verified:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Email not verified!")

    deleted_key = await db_repo.delete_grade(id=id)
    cdn_repo.delete_folder_by_inner_key(key=deleted_key)

    return None

@router.delete('/subject')
async def delete_private_subject(
    id: int,
    cdn_repo: PrivateYandexCDNRepository = Depends(get_cdn_repository(PrivateYandexCDNRepository)),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    user: UserInDB = Depends(get_user_from_token),
    is_superuser = Depends(is_superuser),
    is_verified = Depends(is_verified),
    ) -> None:
    if not user.is_superuser:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not superuser!")
    if not is_verified:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Email not verified!")

    deleted_key = await db_repo.delete_subject(id=id)
    cdn_repo.delete_folder_by_inner_key(key=deleted_key)

    return None

@router.delete('/branch')
async def delete_private_branch(
    id: int,
    cdn_repo: PrivateYandexCDNRepository = Depends(get_cdn_repository(PrivateYandexCDNRepository)),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    user: UserInDB = Depends(get_user_from_token),
    is_superuser = Depends(is_superuser),
    is_verified = Depends(is_verified),
    ) -> None:
    if not user.is_superuser:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not superuser!")
    if not is_verified:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Email not verified!")

    deleted_key = await db_repo.delete_branch(id=id)
    cdn_repo.delete_folder_by_inner_key(key=deleted_key)

    return None

@router.delete('/lecture')
async def delete_private_lecture(
    id: int,
    cdn_repo: PrivateYandexCDNRepository = Depends(get_cdn_repository(PrivateYandexCDNRepository)),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    user: UserInDB = Depends(get_user_from_token),
    is_superuser = Depends(is_superuser),
    is_verified = Depends(is_verified),
    ) -> None:
    if not user.is_superuser:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not superuser!")
    if not is_verified:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Email not verified!")

    deleted_key = await db_repo.delete_lecture(id=id)
    cdn_repo.delete_folder_by_inner_key(key=deleted_key)

    return None

@router.delete('/theory')
async def delete_private_theory(
    id: int,
    cdn_repo: PrivateYandexCDNRepository = Depends(get_cdn_repository(PrivateYandexCDNRepository)),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    user: UserInDB = Depends(get_user_from_token),
    is_superuser = Depends(is_superuser),
    is_verified = Depends(is_verified),
    ) -> None:
    if not user.is_superuser:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not superuser!")
    if not is_verified:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Email not verified!")

    deleted_key = await db_repo.delete_theory(id=id)
    cdn_repo.delete_folder(prefix=deleted_key)

    return None

@router.delete('/practice')
async def delete_private_practice(
    id: int,
    cdn_repo: PrivateYandexCDNRepository = Depends(get_cdn_repository(PrivateYandexCDNRepository)),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    user: UserInDB = Depends(get_user_from_token),
    is_superuser = Depends(is_superuser),
    is_verified = Depends(is_verified),
    ) -> None:
    if not user.is_superuser:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not superuser!")
    if not is_verified:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Email not verified!")

    deleted_key = await db_repo.delete_practice(id=id)
    cdn_repo.delete_folder(prefix=deleted_key)

    return None

@router.delete('/book')
async def delete_private_book(
    id: int,
    cdn_repo: PrivateYandexCDNRepository = Depends(get_cdn_repository(PrivateYandexCDNRepository)),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    user: UserInDB = Depends(get_user_from_token),
    is_superuser = Depends(is_superuser),
    is_verified = Depends(is_verified),
    ) -> None:
    if not user.is_superuser:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not superuser!")
    if not is_verified:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Email not verified!")

    deleted_key = await db_repo.delete_book(id=id)
    cdn_repo.delete_folder_by_inner_key(key=deleted_key)

    return None


# non cdn content
@router.delete('/video/youtube')
async def delete_private_video(
    id: int,
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    user: UserInDB = Depends(get_user_from_token),
    is_superuser = Depends(is_superuser),
    is_verified = Depends(is_verified),
    ) -> None:
    if not user.is_superuser:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not superuser!")
    if not is_verified:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Email not verified!")

    await db_repo.delete_video(id=id)

    return None

# non cdn content
@router.delete('/game')
async def delete_private_game(
    id: int,
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    user: UserInDB = Depends(get_user_from_token),
    is_superuser = Depends(is_superuser),
    is_verified = Depends(is_verified),
    ) -> None:
    if not user.is_superuser:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not superuser!")
    if not is_verified:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Email not verified!")

    await db_repo.delete_game(id=id)

    return None


