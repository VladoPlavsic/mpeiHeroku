from typing import List
from fastapi import APIRouter
from fastapi import Depends
from starlette.status import HTTP_200_OK

from app.db.repositories.about.about import AboutDBRepository

from app.api.dependencies.database import get_db_repository

# response models
from app.models.about import TeamMemberInDBModel
from app.models.about import ContactsInDBModel
from app.models.about import AboutProjectInDBModel

router = APIRouter()

@router.get("/team", response_model=List[TeamMemberInDBModel], name="get:about-team", status_code=HTTP_200_OK)
async def get_team_members(
    db_repo: AboutDBRepository = Depends(get_db_repository(AboutDBRepository)),
    ) -> List[TeamMemberInDBModel]:

    response = await db_repo.select_all_team_members()
    return response

@router.get("/contacts", response_model=List[ContactsInDBModel], name="get:contacts", status_code=HTTP_200_OK)
async def get_contacts(
    db_repo: AboutDBRepository = Depends(get_db_repository(AboutDBRepository)),
    ) -> List[ContactsInDBModel]:

    response = await db_repo.select_all_contacts()
    return response

@router.get("/about_project", response_model=List[AboutProjectInDBModel], name="get:about_project", status_code=HTTP_200_OK)
async def get_about_project(
    db_repo: AboutDBRepository = Depends(get_db_repository(AboutDBRepository)),
    ) -> List[AboutProjectInDBModel]:

    response = await db_repo.select_all_about_project()
    return response
