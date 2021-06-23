from fastapi import APIRouter
from fastapi import Depends

from starlette.status import HTTP_200_OK
from fastapi import HTTPException

from app.api.dependencies.auth import get_user_from_token, is_superuser


from app.db.repositories.users.users import UsersDBRepository
from app.api.dependencies.database import get_db_repository

from app.models.user import PublicUserInDB, UserInDB

from app.models.token import AccessToken
from app.core.config import AWS_SECRET_ACCESS_KEY, AWS_SECRET_KEY_ID

from app.services import auth_service

router = APIRouter()

@router.get("/admin", name="users:check-if-admin", status_code=HTTP_200_OK)
async def get_private_grades(
    is_superuser = Depends(is_superuser),
    ) -> bool:

    # if user is superuser, send them key 
    # for accessing YC s3
    if is_superuser:
        return {"is_superuser": is_superuser, "AWS_SECRET_ACCESS_KEY": AWS_SECRET_ACCESS_KEY, "AWS_SECRET_KEY_ID": AWS_SECRET_KEY_ID}
    else:
        return {"is_superuser": is_superuser, "AWS_SECRET_ACCESS_KEY": None, "AWS_SECRET_KEY_ID": None}


@router.get("/email/confirm")
async def confirm_email(
    user: UserInDB = Depends(get_user_from_token),
    db_repo: UsersDBRepository = Depends(get_db_repository(UsersDBRepository)),
    ) -> PublicUserInDB:
    try:
        if not user.email_verified:
            await db_repo.verify_email(user_id=user.id)

        if not user.is_active:
            return None

        # Create access token (app.services)
        access_token = AccessToken(
            access_token=auth_service.create_access_token_for_user(user=user), token_type='bearer'
        )

        await db_repo.set_jwt_token(user_id=user.id, token=access_token.access_token)

        user.jwt = access_token.access_token

        return PublicUserInDB(**user.dict(), access_token=access_token)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unhandled exception raised in user. Exited with {e}")