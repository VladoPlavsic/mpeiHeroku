from fastapi import APIRouter
from fastapi import Body, Depends
from starlette.status import HTTP_201_CREATED

from app.db.repositories.about.about import AboutDBRepository
from app.cdn.repositories.about.about import AboutYandexCDNRepository

from app.api.dependencies.database import get_db_repository
from app.api.dependencies.cdn import get_cdn_repository
from app.api.dependencies.auth import get_user_from_token, is_verified, is_superuser

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
    user: UserInDB = Depends(get_user_from_token),
    is_superuser = Depends(is_superuser),
    is_verified = Depends(is_verified),
    ) -> TeamMemberInDBModel:
    if not user.is_superuser:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not superuser!")
    if not is_verified:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Email not verified!")

    sharing_link = cdn_repo.get_sharing_links_from_keys(list_of_objects=[{"Key": new_team_member.photo_key}])
    response = await db_repo.insert_our_team(new_team=CreateTeamMemberModel(**new_team_member.dict(), photo_link=sharing_link[new_team_member.photo_key]))
    return response

@router.post("/contacts", response_model=ContactsInDBModel, name="about:post-contacts", status_code=HTTP_201_CREATED)
async def create_contacts(
    new_contact: PostContactsModel = Body(...),
    db_repo: AboutDBRepository = Depends(get_db_repository(AboutDBRepository)),
    user: UserInDB = Depends(get_user_from_token),
    is_superuser = Depends(is_superuser),
    is_verified = Depends(is_verified),
    ) -> ContactsInDBModel:
    if not user.is_superuser:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not superuser!")
    if not is_verified:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Email not verified!")

    response = await db_repo.insert_contacts(new_contacts=new_contact)
    return response

@router.post("/about_project", response_model=AboutProjectInDBModel, name="about:post-about_project", status_code=HTTP_201_CREATED)
async def create_about_project(
    new_about_project: PostAboutProjectModel = Body(...),
    db_repo: AboutDBRepository = Depends(get_db_repository(AboutDBRepository)),
    user: UserInDB = Depends(get_user_from_token),
    is_superuser = Depends(is_superuser),
    is_verified = Depends(is_verified),
    ) -> AboutProjectInDBModel:
    # i don't think i need user here ?? Check it later
    if not user.is_superuser:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not superuser!")
    if not is_verified:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Email not verified!")
        
    response = await db_repo.insert_about_project(new_about_project=new_about_project)
    return response