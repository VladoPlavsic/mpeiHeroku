from fastapi import APIRouter
from fastapi import Body, Depends
from starlette.status import HTTP_200_OK

from app.api.dependencies.database import get_db_repository
from app.db.repositories.about.about import AboutDBRepository
from app.api.dependencies.cdn import get_cdn_repository
from app.cdn.repositories.about.about import AboutYandexCDNRepository
from app.api.dependencies.auth import allowed_or_denied

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
    allowed: bool = Depends(allowed_or_denied),
    ) -> TeamMemberInDBModel:

    if updated.object_key:
        updated_key = cdn_repo.get_sharing_link_from_object_key(object_key=updated.object_key)
        updated.photo_link = updated_key[updated.object_key]

    response = await db_repo.update_team_member(updated=updated)
    return response

@router.put("/contacts", response_model=ContactsInDBModel, name="put:about-contact", status_code=HTTP_200_OK)
async def update_contact(
    updated: UpdateContactsModel = Body(...),
    db_repo: AboutDBRepository = Depends(get_db_repository(AboutDBRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> ContactsInDBModel:

    response = await db_repo.update_contact(updated=updated)
    return response

@router.put("/about_project", response_model=AboutProjectInDBModel, name="put:about-about_contact", status_code=HTTP_200_OK)
async def update_about_project(
    updated: UpdateAboutProjectModel = Body(...),
    db_repo: AboutDBRepository = Depends(get_db_repository(AboutDBRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> AboutProjectInDBModel:

    response = await db_repo.update_about_project(updated=updated)
    return response

