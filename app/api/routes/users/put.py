from fastapi import APIRouter
from fastapi import Body, Depends

from app.db.repositories.users.users import UsersDBRepository
from app.api.dependencies.database import get_db_repository

from app.api.dependencies.auth import get_user_from_token

# YooMoney
import uuid
from yookassa import Configuration, Payment

from app.core.config import YOOMONEY_ACCOUNT_ID, YOOMONEY_SECRET_KEY


router = APIRouter()

# buying grades/subjects
@router.put("/buy/grade")
async def user_buy_grade_access(
    offer_fk: int = Body(..., embed=True),
    user = Depends(get_user_from_token),
    user_repo: UsersDBRepository = Depends(get_db_repository(UsersDBRepository)),
    ) -> None:

    offer_details = await user_repo.get_offer_details(level=0, offer_fk=offer_fk)
    plan_details = await user_repo.get_plan_details(level=0, plan_fk=offer_details.subscription_fk)

    Configuration.account_id = YOOMONEY_ACCOUNT_ID
    Configuration.secret_key = YOOMONEY_SECRET_KEY

    payment = Payment.create({
        "amount": {
            "value": plan_details.price, # use the value from database
            "currency": "RUB"
        },
        "confirmation":{
            "type": "embedded",
        },
        "capture": True,
        "description": plan_details.name
    }, uuid.uuid4())

    await user_repo.create_payment_request(user_fk=user.id, offer_fk=offer_fk, payment_id=payment.id, level=0)

    return payment


@router.put("/buy/subject")
async def user_buy_subject_access(
    offer_fk: int = Body(..., embed=True),
    user = Depends(get_user_from_token),
    user_repo: UsersDBRepository = Depends(get_db_repository(UsersDBRepository)),
    ) -> None:

    offer_details = await user_repo.get_offer_details(level=1, offer_fk=offer_fk)
    plan_details = await user_repo.get_plan_details(level=1, plan_fk=offer_details.subscription_fk)

    Configuration.account_id = YOOMONEY_ACCOUNT_ID
    Configuration.secret_key = YOOMONEY_SECRET_KEY

    payment = Payment.create({
        "amount": {
            "value": plan_details.price, # use the value from database
            "currency": "RUB"
        },
        "confirmation":{
            "type": "embedded",
        },
        "capture": True,
        "description": plan_details.name
    }, uuid.uuid4())

    await user_repo.create_payment_request(user_fk=user.id, offer_fk=offer_fk, payment_id=payment.id, level=1)

    return payment

