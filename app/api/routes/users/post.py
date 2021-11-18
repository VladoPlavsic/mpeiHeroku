from fastapi import APIRouter, Request
from fastapi import Body, BackgroundTasks, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from starlette.status import HTTP_200_OK

from app.models.email import QuestionEmail

from app.api.dependencies.email import send_message, create_confirm_code_msg, create_confirm_link, create_reactivate_profile_email

from app.db.repositories.users.users import UsersDBRepository
from app.api.dependencies.database import get_db_repository
from app.api.dependencies.auth import get_user_from_token, auth_service

from app.api.dependencies.auth import generate_confirmation_code
from app.api.dependencies.crons import handle_deactivated_profiles

from app.models.token import AccessToken, RefreshToken

# request models
from app.models.user import UserCreate

# response models
from app.models.user import PublicUserInDB, UserInDB

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

    if registred and not isinstance(registred, UserInDB):
        # TODO: If user is registered how do we guarantee that he will confirm email before JWT has expired?
        # If we enter here, we need to check if we can get user from JWT if the error sais expired -> create new JWT for user, and update in db!

        # if email is taken but not confirmed, resend confirmation email
        background_tasks.add_task(send_message, subject="Email confirmation. MPEI kids", message_text=create_confirm_link(token=registred, username=new_user.full_name), to=new_user.email)
        raise HTTPException(
                status_code=409,
                detail="This email is already taken but email not confirmed. Confirmation email resent!"
            )
    elif not registred:
        raise HTTPException(
                status_code=409,
                detail="This email is already taken. Login whith that email or register with new one!"
            )

    access_token = AccessToken(
        access_token=auth_service.create_access_token_for_user(user=registred), token_type='bearer'
    )

    await db_repo.set_jwt_token(user_id=registred.id, token=access_token.access_token)

    background_tasks.add_task(send_message, subject="Подтверждение электронной почты", message_text=create_confirm_link(token=access_token.access_token, username=new_user.full_name), to=registred.email)

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

    if not user.is_active:
        raise HTTPException(
            status_code=406,
            detail="This account has been deactivated.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    confirmation_code = generate_confirmation_code()
    confirmation_code = await user_repo.set_confirmation_code(user_id=user.id, confirmation_code=confirmation_code)

    background_tasks.add_task(send_message, subject="Код подтверждения", message_text=create_confirm_code_msg(confirmation_code=confirmation_code), to=user.email)

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

    if not await user_repo.check_code(user_id=user.id, code=confirmation_code) or not confirmation_code:
        raise HTTPException(
            status_code=401,
            detail="Authentication was unsuccessful.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = AccessToken(access_token=auth_service.create_access_token_for_user(user=user), token_type="bearer")
    refresh_token = RefreshToken(refresh_token=auth_service.create_refresh_token_for_user(user=user))

    await user_repo.set_jwt_token(user_id=user.id, token=refresh_token.refresh_token)

    return PublicUserInDB(**user.dict(), access_token=access_token, refresh_token=refresh_token)

@router.post("/refresh/token", response_model=PublicUserInDB)
async def refresh_jw_token(
    refresh_token: str,
    user_repo: UsersDBRepository = Depends(get_db_repository(UsersDBRepository)),
    ) -> PublicUserInDB:
    user = await get_user_from_token(token=refresh_token)
    user = await user_repo.check_refresh_token(user=user, refresh_token=refresh_token)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Could not refresh jwt. Refresh token not valid. Try logging in again",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token = AccessToken(access_token=auth_service.create_access_token_for_user(user=user), token_type="bearer")
    refresh_token = RefreshToken(refresh_token=auth_service.create_refresh_token_for_user(user=user))

    await user_repo.set_jwt_token(user_id=user.id, token=refresh_token.refresh_token)

    return PublicUserInDB(**user.dict(), access_token=access_token, refresh_token=refresh_token)

@router.post("/subscriptions/check/")
async def user_check_expired_subscriptions(
    background_task: BackgroundTasks,
    user_repo: UsersDBRepository = Depends(get_db_repository(UsersDBRepository)),
    ) -> None:

    background_task.add_task(user_repo.check_expired_subscriptions)
    return None

@router.post("/deactivated/check")
async def users_check_deactivated_profiles(
    background_task: BackgroundTasks,
    user_repo: UsersDBRepository = Depends(get_db_repository(UsersDBRepository)),
    ) -> None:

    one_month_warning = await user_repo.select_deactivated_profiles_for_warning_month()
    one_week_warning = await user_repo.select_deactivated_profiles_for_warning_week()
    deletion_profiles = await user_repo.select_deactivated_profiles_for_deletion()

    background_task.add_task(handle_deactivated_profiles, one_month_warning=one_month_warning, one_week_warning=one_week_warning, deletion_profiles=deletion_profiles)
    
    for profile in deletion_profiles:
        await user_repo.delete_profile(user_id=profile.id)
    return None

   
@router.post("/request/profile/reactivate", status_code=HTTP_200_OK)
async def reactivate_profile_request(
    email: str,
    background_task: BackgroundTasks,
    user_repo: UsersDBRepository = Depends(get_db_repository(UsersDBRepository)),
    ) -> None:

    user = await user_repo.get_user_by_email(email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found with given email!",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    reactivate_hash = await user_repo.create_confirmation_hash_for_reactivation(user_id=user.id)
    if not reactivate_hash:
        raise HTTPException(
            status_code=404,
            detail="Profile not deactivated!",
            headers={"WWW-Authenticate": "Bearer"},
        )

    reactivate_url = create_reactivate_profile_email(reactivate_hash=reactivate_hash)
    background_task.add_task(send_message, subject="Reactivate profile request", message_text=f"To reactivate your profile visit this url: {reactivate_url}", to=user.email)
    return None

@router.post("/profile/reactivate", status_code=HTTP_200_OK)
async def reactivate_profile(
    reactivate_hash: str,
    user_repo: UsersDBRepository = Depends(get_db_repository(UsersDBRepository)),
    ) -> None:

    response = await user_repo.activate_profile(reactivation_hash=reactivate_hash)
    if not response:
        raise HTTPException(
            status_code=403,
            detail="Reactivation failed!",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return None

# YooKassa Confirmation Notifications
@router.post("/subscriptions/notifications", status_code=HTTP_200_OK)
async def subscription_notification_hnd(
    background_tasks: BackgroundTasks,
    notification_object: Request = Body(...),
    user_repo: UsersDBRepository = Depends(get_db_repository(UsersDBRepository)),
    ) -> None:

    notification = await notification_object.json()

    if notification["event"] == "payment.succeeded":
        payment_object = await user_repo.get_payment_request(payment_id=notification["object"]["id"])

        # in case we didn't find any payment object for given id send email to administrator with given payment confirmation data
        if not payment_object:
            background_tasks.add_task(send_message, subject="Payment confirmation failed. Required assistence.", message_text=f"There was error in confirming payment request. This might have happened because there was no recorded payment request with given payment ID when the notification was raised. Notification detail: {notification}")
            return None
        
        product = await user_repo.get_offer_details(level=int(payment_object.level), offer_fk=payment_object.offer_fk)
        # add product
        subscription_details = await user_repo.add_product_to_user(user_id=payment_object.user_fk, product_id=product.product_fk, subscription_fk=payment_object.offer_fk, level=int(payment_object.level))
        user = await user_repo.get_user_by_id(user_id=payment_object.user_fk)
        if subscription_details.for_life:
            background_tasks.add_task(send_message, subject="Payment confirmation.", message_text=f"Payment successfully processed. You have access to {subscription_details.plan_name} for life.", to=user.email)
        else:
            background_tasks.add_task(send_message, subject="Payment confirmation.", message_text=f"Payment successfully processed. You have access to {subscription_details.plan_name} until {subscription_details.expiration_date}", to=user.email)

        await user_repo.delete_pending_subscription(payment_id=notification["object"]["id"])
   
    elif notification["event"] == "payment.canceled":
        await user_repo.delete_pending_subscription(payment_id=notification["object"]["id"])

    return None
