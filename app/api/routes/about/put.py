from fastapi import APIRouter
from fastapi import Body, Depends
from starlette.status import HTTP_200_OK

from app.api.dependencies.database import get_db_repository
from app.db.repositories.about.about import AboutDBRepository
from app.api.dependencies.cdn import get_cdn_repository
from app.cdn.repositories.about.about import AboutYandexCDNRepository
from app.api.dependencies.auth import get_user_from_token, is_superuser, is_verified

# request models
from app.models.about import UpdateTeamMemberModel
from app.models.about import UpdateAboutProjectModel
from app.models.about import UpdateContactsModel

# respoonse models
from app.models.about import TeamMemberInDBModel
from app.models.about import AboutProjectInDBModel
from app.models.about import ContactsInDBModel

from app.models.user import UserInDB

router = APIRouter()


#TODO: On update photo delete old key!!!
@router.put("/team", response_model=TeamMemberInDBModel, name="put:about-team", status_code=HTTP_200_OK)
async def update_team_member(
    updated: UpdateTeamMemberModel = Body(...),
    db_repo: AboutDBRepository = Depends(get_db_repository(AboutDBRepository)),
    cdn_repo: AboutYandexCDNRepository = Depends(get_cdn_repository(AboutYandexCDNRepository)),
    user: UserInDB = Depends(get_user_from_token),
    is_superuser = Depends(is_superuser),
    is_verified = Depends(is_verified),
    ) -> TeamMemberInDBModel:
    if not user.is_superuser:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not superuser!")
    if not is_verified:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Email not verified!")

    if updated.photo_key:
        updated_key = cdn_repo.get_sharing_links_from_keys(list_of_objects=[{"Key": updated.photo_key}])
        updated.photo_link = updated_key[updated.photo_key]

    response = await db_repo.update_team_member(updated=updated)
    return response

@router.put("/contacts", response_model=ContactsInDBModel, name="put:about-contact", status_code=HTTP_200_OK)
async def update_contact(
    updated: UpdateContactsModel = Body(...),
    db_repo: AboutDBRepository = Depends(get_db_repository(AboutDBRepository)),
    user: UserInDB = Depends(get_user_from_token),
    is_superuser = Depends(is_superuser),
    is_verified = Depends(is_verified),
    ) -> ContactsInDBModel:
    if not user.is_superuser:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not superuser!")
    if not is_verified:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Email not verified!")

    response = await db_repo.update_contact(updated=updated)
    return response

@router.put("/about_project", response_model=AboutProjectInDBModel, name="put:about-about_contact", status_code=HTTP_200_OK)
async def update_about_project(
    updated: UpdateAboutProjectModel = Body(...),
    db_repo: AboutDBRepository = Depends(get_db_repository(AboutDBRepository)),
    user: UserInDB = Depends(get_user_from_token),
    is_superuser = Depends(is_superuser),
    is_verified = Depends(is_verified),
    ) -> AboutProjectInDBModel:
    if not user.is_superuser:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not superuser!")
    if not is_verified:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Email not verified!")

    response = await db_repo.update_about_project(updated=updated)
    return response

