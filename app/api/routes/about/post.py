from fastapi import APIRouter
from fastapi import Body, Depends
from starlette.status import HTTP_201_CREATED

from app.db.repositories.about.about import AboutDBRepository
from app.cdn.repositories.about.about import AboutYandexCDNRepository

from app.api.dependencies.database import get_db_repository
from app.api.dependencies.cdn import get_cdn_repository
from app.api.dependencies.auth import allowed_or_denied

# post models
from app.models.about import PostTeamMemberModel
from app.models.about import PostAboutProjectModel
from app.models.about import PostContactsModel
from app.models.about import CreateTeamMemberModel

# response models
from app.models.about import TeamMemberInDBModel
from app.models.about import AboutProjectInDBModel
from app.models.about import ContactsInDBModel

from app.models.user import UserInDB

router = APIRouter()

@router.post("/team", response_model=TeamMemberInDBModel, name="about:post-team-member", status_code=HTTP_201_CREATED)
async def create_about_team(
    new_team_member: PostTeamMemberModel = Body(...),
    db_repo: AboutDBRepository = Depends(get_db_repository(AboutDBRepository)),
    cdn_repo: AboutYandexCDNRepository = Depends(get_cdn_repository(AboutYandexCDNRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> TeamMemberInDBModel:

    shared = cdn_repo.get_sharing_link_from_object_key(object_key=new_team_member.object_key)
    new_team_member = CreateTeamMemberModel(**new_team_member.dict(), photo_link=shared[new_team_member.object_key])
    response = await db_repo.insert_team_member(new_team=new_team_member)
    return response

@router.post("/contacts", response_model=ContactsInDBModel, name="about:post-contacts", status_code=HTTP_201_CREATED)
async def create_contacts(
    new_contact: PostContactsModel = Body(...),
    db_repo: AboutDBRepository = Depends(get_db_repository(AboutDBRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> ContactsInDBModel:
    
    response = await db_repo.insert_contacts(new_contacts=new_contact)
    return response

@router.post("/about_project", response_model=AboutProjectInDBModel, name="about:post-about_project", status_code=HTTP_201_CREATED)
async def create_about_project(
    new_about_project: PostAboutProjectModel = Body(...),
    db_repo: AboutDBRepository = Depends(get_db_repository(AboutDBRepository)),
    allowed: bool = Depends(allowed_or_denied),
    ) -> AboutProjectInDBModel:
        
    response = await db_repo.insert_about_project(new_about_project=new_about_project)
    return response