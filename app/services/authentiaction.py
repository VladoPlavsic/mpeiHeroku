from typing import Optional
import jwt
import bcrypt
from datetime import datetime, timedelta
from passlib.context import CryptContext

from fastapi import HTTPException, status
from pydantic import ValidationError

from app.core.config import SECRET_KEY, JWT_ALGORITHM, JWT_AUDIENCE, JWT_TOKEN_PREFIX, ACCESS_TOKEN_EXPIRE_MINUTES
from app.models.token import JWTMeta, JWTCreds, JWTPayload, JWTUserMeta
from app.models.user import UserPasswordUpdate, UserInDB

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class AuthException(BaseException):
    """
    Custom auth exception that can be modified later on.
    """
    pass

class AuthService:
    def create_salt_and_hash_password(self, *, plaintext_password: str) -> UserPasswordUpdate:
        salt = self.generate_salt()

        hashed_password = self.hash_password(password=plaintext_password, salt=salt)

        return UserPasswordUpdate(salt=salt, password=hashed_password)

    def generate_salt(self) -> str:
        return bcrypt.gensalt().decode()

    def hash_password(self, password: str, salt: str) -> str:
        return pwd_context.hash(password + salt)

    def verify_password(self, *, password: str, salt: str, hashed_password: str) -> bool:
        return pwd_context.verify(password + salt, hashed_password)

    def create_access_token_for_user(
        self,
        *,
        user: UserInDB,
        secret_key: str = str(SECRET_KEY),
        audience: str = JWT_AUDIENCE,
        expires_in: int = ACCESS_TOKEN_EXPIRE_MINUTES,
        ) -> str:
        if not user or not isinstance(user, UserInDB):
            return None

        jwt_meta = JWTMeta(
            aud=audience,
            iat=datetime.timestamp(datetime.utcnow()),
            exp=datetime.timestamp(datetime.utcnow() + timedelta(minutes=expires_in)),
        )
        jwt_creds = JWTCreds(email=user.email, phone_number=user.phone_number)
        jwt_user_meta = JWTUserMeta(**user.dict())

        token_payload = JWTPayload(
            **jwt_meta.dict(),
            **jwt_creds.dict(),
            **jwt_user_meta.dict(),
        )

        access_token = jwt.encode(token_payload.dict(), secret_key, algorithm=JWT_ALGORITHM)
        return access_token

    def create_refresh_token_for_user(self,
        *,
        user: UserInDB,
        secret_key: str = str(SECRET_KEY),
        audience: str = JWT_AUDIENCE,
        expires_in: int = 60 * 24 * 365, # refresh token expires in a year
        ) -> str:
        if not user or not isinstance(user, UserInDB):
            return None

        jwt_meta = JWTMeta(
            aud=audience,
            iat=datetime.timestamp(datetime.utcnow()),
            exp=datetime.timestamp(datetime.utcnow() + timedelta(minutes=expires_in)),
        )
        jwt_creds = JWTCreds(email=user.email, phone_number=user.phone_number)
        user.email_verified = False
        jwt_user_meta = JWTUserMeta(**user.dict())

        token_payload = JWTPayload(
            **jwt_meta.dict(),
            **jwt_creds.dict(),
            **jwt_user_meta.dict(),
        )

        refresh_token = jwt.encode(token_payload.dict(), secret_key, algorithm=JWT_ALGORITHM)
        return refresh_token

    def get_user_from_token(self, *, token: str, secret_key: str) -> Optional[str]:
        """Takes in JWT token. Returns user (encoded in token) || 401"""
        try:
            decoded_token = jwt.decode(token, str(secret_key), audience=JWT_AUDIENCE, algorithms=[JWT_ALGORITHM])
            payload = JWTPayload(**decoded_token)
        except (jwt.PyJWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate token credientals",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return payload