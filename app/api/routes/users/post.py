from fastapi import APIRouter, Request
from fastapi import Body, BackgroundTasks, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from starlette.status import HTTP_200_OK


from app.models.email import QuestionEmail

from app.api.dependencies.email import send_message, create_confirm_code_msg, create_confirm_link

from app.db.repositories.users.users import UsersDBRepository
from app.api.dependencies.database import get_db_repository

from app.api.dependencies.auth import generate_confirmation_code

from app.models.token import AccessToken
from app.services import auth_service

# request models
from app.models.user import UserCreate

# response models
from app.models.user import PublicUserInDB

router = APIRouter()

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

@router.post("/subscriptions/check/")
async def user_check_expired_subscriptions(
    background_task: BackgroundTasks,
    user_repo: UsersDBRepository = Depends(get_db_repository(UsersDBRepository)),
    ) -> None:

    background_task.add_task(user_repo.check_expired_subscriptions)
    return None

# YooKassa Confirmation Notifications
@router.post("/subscriptions/notifications", status_code=HTTP_200_OK)
async def subscription_notification_hnd(
    background_tasks: BackgroundTasks,
    notification_object: Request = Body(...),
    user_repo: UsersDBRepository = Depends(get_db_repository(UsersDBRepository)),
    ) -> None:

    print(notification_object)
    notification = await notification_object.json()
    print(notification)

    if notification["event"] == "payment.succeeded":
        payment_object = await user_repo.get_payment_request(payment_id=notification["object"]["id"])

        # in case we didn't find any payment object for given id
        if not payment_object:
            background_tasks.add_task(send_message, subject="Payment confirmation failed. Required assistence.", message_text=f"There was error in confirming payment request. This might have happened because there was no recorded payment request with given payment ID when the notification was raised. Notification detail: {notification}")
            return None
            
        product = await user_repo.get_offer_details(level=int(payment_object.level), offer_fk=payment_object.offer_fk)
        # add product
        await user_repo.add_product_to_user(user_id=payment_object.user_fk, product_id=product.product_fk, subscription_fk=payment_object.offer_fk, level=int(payment_object.level))
        await user_repo.delete_pending_subscription(payment_id=notification["object"]["id"])
   
    elif notification["event"] == "payment.canceled":
        await user_repo.delete_pending_subscription(payment_id=notification["object"]["id"])

    return None

# TODO:
# ###
# 1. Create a route for notifications
# 4. Delete realy old pending statuses
