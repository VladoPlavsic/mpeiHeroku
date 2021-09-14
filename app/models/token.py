from datetime import datetime, timedelta
from pydantic import EmailStr
from app.core.config import JWT_AUDIENCE, ACCESS_TOKEN_EXPIRE_MINUTES
from app.models.core import BaseModel


class JWTMeta(BaseModel):
    iss: str = "mpei.ru"
    aud: str = JWT_AUDIENCE
    iat: float = datetime.timestamp(datetime.utcnow())
    exp: float = datetime.timestamp(datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

class JWTCreds(BaseModel):
    """How we'll identify users"""
    email: EmailStr
    phone_number: str

class JWTUserMeta(BaseModel):
    """All about user"""
    id: int
    city: str
    school: str
    email_verified: bool
    is_superuser: bool


class JWTPayload(JWTMeta, JWTCreds, JWTUserMeta):
    """
    JWT Payload right before it's encoded - combine meta and username
    """
    pass

class AccessToken(BaseModel):
    access_token: str
    token_type: str

class RefreshToken(BaseModel):
    refresh_token: str
