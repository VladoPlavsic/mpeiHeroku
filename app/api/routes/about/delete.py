from fastapi import APIRouter
from fastapi import Depends, Path, HTTPException

from starlette.status import HTTP_200_OK

from app.api.dependencies.database import get_db_repository
from app.api.dependencies.cdn import get_cdn_repository

from app.api.dependencies.auth import allowed_or_denied

from app.db.repositories.about.about import AboutDBRepository
from app.cdn.repositories.about.about import AboutYandexCDNRepository

from app.models.user import UserInDB

router = APIRouter()

@router.delete("/team/{order}", response_model=None, name="delete:about-team", status_code=HTTP_200_OK)
async def delete_team_member(
    order: int = Path(...),
    db_repo: AboutDBRepository = Depends(get_db_repository(AboutDBRepository)),
    cdn_repo: AboutYandexCDNRepository = Depends(get_cdn_repository(AboutYandexCDNRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> None:

    deleted_key = await db_repo.delete_team_member(id=order)
    if deleted_key:
        cdn_repo.delete_key(key=deleted_key)

    return None


@router.delete("/contacts/{order}", response_model=None, name="delete:about-contact", status_code=HTTP_200_OK)
async def delete_contact(
    order: int = Path(...),
    db_repo: AboutDBRepository = Depends(get_db_repository(AboutDBRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> None:

    await db_repo.delete_contact(id=order)
    return None

@router.delete("/about_project/{order}", response_model=None, name="delete:about-about_project", status_code=HTTP_200_OK)
async def delete_about_project(
    order: int = Path(...),
    db_repo: AboutDBRepository = Depends(get_db_repository(AboutDBRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> None:

    await db_repo.delete_about_project(id=order)
    return None

