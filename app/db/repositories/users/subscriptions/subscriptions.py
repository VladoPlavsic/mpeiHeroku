from typing import List, Union

from app.db.repositories.base import BaseDBRepository

from app.models.private import OfferDetails
from app.models.private import AvailableSubjectSubscriptionPlans
from app.models.private import AvailableGradeSubscriptionPlans
from app.models.private import PaymentRequestDetails

from app.db.repositories.users.subscriptions.queries import *


class UsersDBSubscriptionsRepository(BaseDBRepository):
    async def create_payment_request(self, *, user_fk: int, offer_fk: int, payment_id: str, level: int, confirmation_token: str) -> None:
        await self._fetch_one(query=create_payment_request_query(user_fk=user_fk, offer_fk=offer_fk, payment_id=payment_id, level=level, confirmation_token=confirmation_token))

    async def check_payment_request(self, *, user_fk: int, offer_fk: int, level: int) -> str:
        payment_id = await self._fetch_one(query=check_payment_request_query(user_fk=user_fk, offer_fk=offer_fk, level=level))
        return payment_id['payment_id'] if payment_id else None

    async def get_payment_request(self, *, payment_id: str) -> PaymentRequestDetails:
        response = await self._fetch_one(query=get_payment_request_query(payment_id=payment_id))
        return PaymentRequestDetails(**response) if response else None

    # LEVEL: 0 - grade | 1 - subjects
    async def get_offer_details(self, *, level: int, offer_fk: int) -> OfferDetails:
        response = await self._fetch_one(query=get_offer_details_query(level=level, offer_fk=offer_fk))
        return OfferDetails(**response)

    async def get_plan_details(self, *, level: int, plan_fk: int) -> Union[AvailableGradeSubscriptionPlans, AvailableSubjectSubscriptionPlans]:
        response = await self._fetch_one(query=get_plan_details_query(level=level, plan_fk=plan_fk))
        return AvailableSubjectSubscriptionPlans(**response) if level else AvailableGradeSubscriptionPlans(**response)

    async def check_expired_subscriptions(self) -> None:
        await self._execute_one(query=delete_expired_subscriptions_query()) 

    async def delete_pending_subscription(self, *, payment_id: str) -> None:
        await self._execute_one(query=delete_pending_subscripiton_query(payment_id=payment_id))
        