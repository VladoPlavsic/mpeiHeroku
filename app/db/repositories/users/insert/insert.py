from app.db.repositories.base import BaseDBRepository

from app.db.repositories.users.insert.queries import *

from app.models.user import UserCreate
from app.models.user import UserInDB, UserInDB

class UsersDBInsertRepository(BaseDBRepository):

    async def register_new_user(self, new_user: UserCreate) -> UserInDB:
        # make sure email is not taken
        user = await self.get_user_by_email(email=new_user.email)
        if user:
            # if user is taken and email not confirmed, return already generated confirmation link
            if not user.email_verified:
                return user.jwt
            else:
                return None
                        
        user_password_update = self.auth_service.create_salt_and_hash_password(plaintext_password=new_user.password)
        new_user_params = new_user.copy(update=user_password_update.dict())
        registred = await self._fetch_one(query=register_new_user_query(**new_user_params.dict()))

        return UserInDB(**registred)

    async def set_jwt_token(self, *, user_id: int, token: str):
        await self._execute_one(query=set_jwt_token_query(user_id=user_id, token=token))

    async def verify_email(self, *, user_id: int):
        await self._execute_one(query=verify_email_query(user_id=user_id))

    async def add_product_to_user(self, *, user_id: int, product_id: int, subscription_fk: int , level: int):
        """We add one of our products to user.

        Keyword params:
        user_id         -- ID of a user we want to add product to
        product_id      -- ID of a product we want to add to user
        subscription_fk -- ID of a subscription type we are adding to user (lenght of a subscription)
        level           -- 0 | 1 - determins if we are trying to add grades or subjects:
            0 - grades
            1 - subjects
        """
        if not level:
            await self._execute_one(query=add_grade_to_user_query(user_id=user_id, grade_id=product_id, subscription_fk=subscription_fk))
        else:
            await self._execute_one(query=add_subject_to_user_query(user_id=user_id, subject_id=product_id, subscription_fk=subscription_fk))

    async def set_confirmation_code(self, *, user_id: int, confirmation_code: str) -> str:
        response = await self._fetch_one(query=set_confirmation_code_query(user_id=user_id, confirmation_code=confirmation_code))
        return response["code"]
