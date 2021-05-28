from typing import List, Union
from fastapi import HTTPException

from app.db.repositories.base import BaseDBRepository

from app.models.private import OfferDetails
from app.models.private import AvailableSubjectSubscriptionPlans
from app.models.private import AvailableGradeSubscriptionPlans
from app.models.private import PaymentRequestDetails

from app.db.repositories.users.subscriptions.queries import *

import logging

logger = logging.getLogger(__name__)

class UserDBSubscriptionsRepository(BaseDBRepository):
    async def create_payment_request(self, *, user_fk: int, offer_fk: int, payment_id: str, level: int) -> None:
        exists = await self.__execute(query=check_payment_request_query(user_fk=user_fk, offer_fk=offer_fk, level=level))
        if exists['pending']:
            raise HTTPException(status_code=409, detail="Already pending!")
        await self.__execute(query=create_payment_request_query(user_fk=user_fk, offer_fk=offer_fk, payment_id=payment_id, level=level))

    async def get_payment_request(self, *, payment_id: str) -> PaymentRequestDetails:
        response = await self.__execute(query=get_payment_request_query(payment_id=payment_id))
        return PaymentRequestDetails(**response)

    # LEVEL: 0 - grade | 1 - subjects
    async def get_offer_details(self, *, level: int, offer_fk: int) -> OfferDetails:
        response = await self.__execute(query=get_offer_details_query(level=level, offer_fk=offer_fk))
        return OfferDetails(**response)

    async def get_plan_details(self, *, level: int, plan_fk: int) -> Union[AvailableGradeSubscriptionPlans, AvailableSubjectSubscriptionPlans]:
        response = await self.__execute(query=get_plan_details_query(level=level, plan_fk=plan_fk))
        logger.warn(plan_fk)
        return AvailableSubjectSubscriptionPlans(**response) if level else AvailableGradeSubscriptionPlans(**response)

    async def check_expired_subscriptions(self) -> None:
        await self.__execute(query=delete_expired_subscriptions_query()) 

    async def delete_pending_subscription(self, *, payment_id: str) -> None:
        await self.__execute(query=delete_pending_subscripiton_query(payment_id=payment_id))
        
    async def __execute(self, *, query): 
        try:
            response = await self.db.fetch_one(query=query)
        except Exception as e:
            logger.error("ERROR IN USER INSERT REPOSITORY")
            logger.error(e)
            logger.error("ERROR IN USER INSERT REPOSITORY")            
            raise HTTPException(status_code=400, detail=f"Unhandled exception raised in user insert repository. Exited with {e}")

        return response
