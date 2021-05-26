from fastapi import APIRouter
from fastapi import Body, BackgroundTasks, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from starlette.status import HTTP_200_OK

from app.models.email import QuestionEmail
from app.models.email import EmailResponse

from app.api.dependencies.email import send_message, create_confirm_code_msg, create_confirm_link

from app.db.repositories.users.users import UsersDBRepository
from app.api.dependencies.database import get_db_repository

from app.api.dependencies.auth import generate_confirmation_code

from app.models.token import AccessToken
from app.services import auth_service

from app.api.dependencies.auth import get_user_from_token, is_superuser

# request models
from app.models.user import UserCreate

# response models
from app.models.user import PublicUserInDB, UserInDB

router = APIRouter()


@router.get("/admin", name="users:check-if-admin", status_code=HTTP_200_OK)
async def get_private_grades(
    user: UserInDB = Depends(get_user_from_token),
    is_superuser = Depends(is_superuser),
    ):

    return is_superuser

@router.post("/email/contact")
async def send_user_question_via_email(
    background_tasks: BackgroundTasks,
    email: QuestionEmail = Body(..., embed=True),
    ) -> None:

    background_tasks.add_task(send_message, subject=email.user_email, message_text=email.email_body)

    return None

@router.post("/register")
async def register_new_user(
    background_tasks: BackgroundTasks,
    new_user: UserCreate = Body(...),
    db_repo: UsersDBRepository = Depends(get_db_repository(UsersDBRepository)),
    ) -> PublicUserInDB:
    registred = await db_repo.register_new_user(new_user=new_user)

    access_token = AccessToken(
        access_token=auth_service.create_access_token_for_user(user=registred), token_type='bearer'
    )

    await db_repo.set_jwt_token(user_id=registred.id, token=access_token.access_token)

    background_tasks.add_task(send_message, subject="Email confirmation. MPEI kids", message_text=create_confirm_link(token=access_token.access_token), to=registred.email)

    return PublicUserInDB(**registred.dict())

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

@router.post("/login/code", status_code=HTTP_200_OK)
async def user_login_with_email_and_password_send_code(
    background_tasks: BackgroundTasks,
    user_repo: UsersDBRepository = Depends(get_db_repository(UsersDBRepository)),
    form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm),
    ):
    user = await user_repo.authenticate_user(email=form_data.username, password=form_data.password)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Authentication was unsuccessful.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.email_verified:
        raise HTTPException(
            status_code=403,
            detail="Email not verified. Please verify and try again.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    confirmation_code = generate_confirmation_code()
    await user_repo.set_confirmation_code(user_id=user.id, confirmation_code=confirmation_code)

    background_tasks.add_task(send_message, subject="Confirmation code.", message_text=create_confirm_code_msg(confirmation_code=confirmation_code), to=user.email)

    return {"Detail": "Confirmation code email sent!"}

@router.post("/login/token/", response_model=PublicUserInDB)
async def user_login_with_email_and_password(
    confirmation_code: str,
    user_repo: UsersDBRepository = Depends(get_db_repository(UsersDBRepository)),
    form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm),
    ) -> PublicUserInDB:
    user = await user_repo.authenticate_user(email=form_data.username, password=form_data.password)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Authentication was unsuccessful.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if confirmation_code != user.confirmation_code:
        raise HTTPException(
            status_code=401,
            detail="Authentication was unsuccessful.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = AccessToken(access_token=auth_service.create_access_token_for_user(user=user), token_type="bearer")

    await user_repo.set_jwt_token(user_id=user.id, token=access_token.access_token)

    return PublicUserInDB(**user.dict(), access_token=access_token)


# buying grades/subjects
@router.post("/buy/grade")
async def user_buy_grade_access(
    grade_id: int = Body(..., embed=True),
    user = Depends(get_user_from_token),
    user_repo: UsersDBRepository = Depends(get_db_repository(UsersDBRepository)),
    ) -> None:

    # remove default days
    await user_repo.add_grade_to_user(user_id=user.id, grade_id=grade_id, days=200)

    return None

@router.post("/buy/subject")
async def user_buy_subject_access(
    subject_id: int = Body(..., embed=True),
    user = Depends(get_user_from_token),
    user_repo: UsersDBRepository = Depends(get_db_repository(UsersDBRepository)),
    ) -> None:

    # remove default days
    await user_repo.add_subject_to_user(user_id=user.id, subject_id=subject_id, days=200)

    return None

# get
@router.get("/user")
async def user_get_user(
    user = Depends(get_user_from_token),
    user_repo: UsersDBRepository = Depends(get_db_repository(UsersDBRepository)),
) -> None:

    return await user_repo.get_user_by_email(email=user.email)