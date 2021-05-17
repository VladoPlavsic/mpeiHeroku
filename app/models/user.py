import string
from datetime import datetime
from typing import Optional, Any
from pydantic import EmailStr, constr, validator
from app.models.core import BaseModel
from app.models.token import AccessToken

class UserBase(BaseModel):
    """
    Leaving off password and salt from base model
    """
    email: Optional[EmailStr]
    phone_number: str
    city: str
    school: str
    email_verified: bool = False
    is_active: bool = False
    is_superuser: bool = False

class UserCreate(BaseModel):
    """
    Email, username, and password are required for registering a new user
    """
    email: EmailStr
    phone_number: str
    city: str
    school: str
    password: constr(min_length=7, max_length=100)
    full_name: str

class UserUpdate(BaseModel):
    """
    Users are allowed to update their email
    """
    email: Optional[EmailStr]

class UserPasswordUpdate(BaseModel):
    """
    Users can change their password
    """
    password: constr(min_length=7, max_length=100)
    salt: str

class UserInDB(UserBase):
    """
    Add in id, created_at, updated_at, and user's password and salt
    """
    id: int
    password: constr(min_length=7, max_length=100)
    salt: str
    confirmation_code: Optional[str]
    jwt: Optional[str]

class PublicUserInDB(UserBase):
    id: int
    access_token: Optional[AccessToken]


# availble subjects/grades
class UserAvailableGrades(BaseModel):
    grade_id: int
    crated_at: Any
    updated_at: Any

class UserAvailableSubjects(BaseModel):
    subject_id: int
    created_at: datetime
    updated_at: datetime