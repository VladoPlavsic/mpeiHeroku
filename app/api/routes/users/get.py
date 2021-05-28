from fastapi import APIRouter
from fastapi import Depends

from starlette.status import HTTP_200_OK

from app.api.dependencies.auth import get_user_from_token, is_superuser

from app.db.repositories.users.users import UsersDBRepository
from app.api.dependencies.database import get_db_repository

from app.models.user import PublicUserInDB, UserInDB

from app.models.token import AccessToken

router = APIRouter()

@router.get("/admin", name="users:check-if-admin", status_code=HTTP_200_OK)
async def get_private_grades(
    is_superuser = Depends(is_superuser),
    ) -> bool:

    return is_superuser

@router.get("/email/confirm")
async def confirm_email(
    user: UserInDB = Depends(get_user_from_token),
    db_repo: UsersDBRepository = Depends(get_db_repository(UsersDBRepository)),
    ) -> AccessToken:
    if not user.email_verified:
        await db_repo.verify_email(user_id=user.id)

    if not user.is_active:
        return None

    access_token = AccessToken(
        access_token=auth_service.create_access_token_for_user(user=user), token_type='bearer'
    )

    await db_repo.set_jwt_token(user_id=user.id, token=access_token.access_token)

    user.jwt = access_token.access_token

    return PublicUserInDB(**user.dict(), access_token=access_token)