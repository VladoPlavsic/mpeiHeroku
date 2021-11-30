from fastapi import APIRouter
from fastapi import Depends

from starlette.status import HTTP_200_OK
from fastapi import HTTPException

from app.api.dependencies.auth import get_user_from_token, is_superuser


from app.db.repositories.users.users import UsersDBRepository
from app.api.dependencies.database import get_db_repository

from app.models.user import PublicUserInDB, UserInDB, AdminAvailableData
from app.models.user import SubscriptionHistory
from app.models.user import ActiveSubscriptions

from app.models.token import AccessToken
from app.core.config import AWS_SECRET_ACCESS_KEY, AWS_SECRET_KEY_ID

from app.services import auth_service

router = APIRouter()

@router.get("/admin", name="users:check-if-admin", status_code=HTTP_200_OK)
async def get_private_grades(
    is_superuser = Depends(is_superuser),
    ) -> bool:

    """If user is superuser, send them secrets for accessing YC s3"""
    response = AdminAvailableData(is_superuser=is_superuser, AWS_SECRET_ACCESS_KEY=None, AWS_SECRET_KEY_ID=None)

    if is_superuser:
        response.AWS_SECRET_ACCESS_KEY = AWS_SECRET_ACCESS_KEY
        response.AWS_SECRET_KEY_ID = AWS_SECRET_KEY_ID

    return response


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

@router.get("/profile")
async def get_user_information(
    user: UserInDB = Depends(get_user_from_token),
    db_repo: UsersDBRepository = Depends(get_db_repository(UsersDBRepository)),
    ) -> PublicUserInDB:

    response = await db_repo.get_user_by_id(user_id=user.id)
    return PublicUserInDB(**response.dict())

@router.get("/subscription/history")
async def get_subscription_history(
    user: UserInDB = Depends(get_user_from_token),
    db_repo: UsersDBRepository = Depends(get_db_repository(UsersDBRepository)),
    ) -> SubscriptionHistory:

    return await db_repo.get_subscription_history(user_id=user.id)

@router.get("/active/subscriptions")
async def get_active_subscriptions(
    user: UserInDB = Depends(get_user_from_token),
    db_repo: UsersDBRepository = Depends(get_db_repository(UsersDBRepository)),
    ) -> ActiveSubscriptions:

    return await db_repo.get_active_subscriptions(user_id=user.id)