from fastapi import APIRouter
from fastapi import Depends, Path

from starlette.status import HTTP_200_OK

from app.api.dependencies.database import get_db_repository

from app.api.dependencies.auth import get_user_from_token, is_superuser, is_verified

from app.db.repositories.about.about import AboutDBRepository

from app.models.user import UserInDB

router = APIRouter()

@router.delete("/team/{order}", response_model=None, name="delete:about-team", status_code=HTTP_200_OK)
async def delete_team_member(
    order: int = Path(...),
    db_repo: AboutDBRepository = Depends(get_db_repository(AboutDBRepository)),
    user: UserInDB = Depends(get_user_from_token),
    is_superuser = Depends(is_superuser),
    is_verified = Depends(is_verified),
    ) -> None:
    if not user.is_superuser:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not superuser!")
    if not is_verified:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Email not verified!")
    
    await db_repo.delete_team_member(id=order)


@router.delete("/contacts/{order}", response_model=None, name="delete:about-contact", status_code=HTTP_200_OK)
async def delete_contact(
    order: int = Path(...),
    db_repo: AboutDBRepository = Depends(get_db_repository(AboutDBRepository)),
    user: UserInDB = Depends(get_user_from_token),
    is_superuser = Depends(is_superuser),
    is_verified = Depends(is_verified),
    ) -> None:
    if not user.is_superuser:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not superuser!")
    if not is_verified:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Email not verified!")

    await db_repo.delete_contact(id=order)

@router.delete("/about_project/{order}", response_model=None, name="delete:about-about_project", status_code=HTTP_200_OK)
async def delete_about_project(
    order: int = Path(...),
    db_repo: AboutDBRepository = Depends(get_db_repository(AboutDBRepository)),
    user: UserInDB = Depends(get_user_from_token),
    is_superuser = Depends(is_superuser),
    is_verified = Depends(is_verified),
    ) -> None:
    if not user.is_superuser:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not superuser!")
    if not is_verified:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Email not verified!")

    await db_repo.delete_about_project(id=order)

