import string
from datetime import datetime
from typing import Optional, Any, List
from pydantic import EmailStr, constr, validator
from app.models.core import BaseModel, DBCoreModel
from app.models.token import AccessToken, RefreshToken

class UserBase(BaseModel):
    """Leaving off password and salt from base model"""
    email: Optional[EmailStr]
    phone_number: str
    city: str
    school: str
    email_verified: bool = False
    is_active: bool = True
    is_superuser: bool = False

class UserCreate(BaseModel):
    """Email, username, and password are required for registering a new user"""
    email: EmailStr
    phone_number: str
    city: str
    school: str
    password: constr(min_length=7, max_length=100)
    full_name: str

class UserUpdate(BaseModel):
    """Users are allowed to update their personal data, except email"""
    full_name: Optional[str]
    phone_number: Optional[str]
    city: Optional[str]
    school: Optional[str]

class UserPasswordUpdate(BaseModel):
    """Users can change their password"""
    password: constr(min_length=7, max_length=100)
    salt: str

class UserInDB(UserBase):
    """Add in id, created_at, updated_at, and user's password and salt"""
    id: int
    password: constr(min_length=7, max_length=100)
    salt: str
    confirmation_code: Optional[str]
    jwt: Optional[str]
    full_name: str

class PublicUserInDB(UserBase):
    id: int
    access_token: Optional[AccessToken]
    refresh_token: Optional[RefreshToken]
    full_name: Optional[str]

# availble subjects/grades
class UserAvailableGrades(BaseModel):
    grade_id: int
    crated_at: Any
    updated_at: Any

class UserAvailableSubjects(BaseModel):
    subject_id: int
    created_at: datetime
    updated_at: datetime

class AdminAvailableData(BaseModel):
    is_superuser: bool
    AWS_SECRET_KEY_ID: Optional[str]
    AWS_SECRET_ACCESS_KEY: Optional[str]
    
class UserDeletion(BaseModel):
    id: int
    email: Optional[EmailStr]

class ActiveSubscriptionInformationCore(DBCoreModel):
    class_name: str
    expiration_date: datetime
    for_life: bool

class ActiveSubscriptionInformationGrade(ActiveSubscriptionInformationCore):
    pass

class ActiveSubscriptionInformationSubject(ActiveSubscriptionInformationCore):
    subject_name: str

class ActiveSubscriptions(DBCoreModel):
    grades: List[ActiveSubscriptionInformationGrade]
    subjects: List[ActiveSubscriptionInformationSubject]

class SubscriptionHistoryUnit(DBCoreModel):
    name_ru: str
    price: float
    purchased_at: datetime
    month_count: int    

class SubscriptionHistory(DBCoreModel):
    grades: List[SubscriptionHistoryUnit]
    subjects: List[SubscriptionHistoryUnit]
class SubscriptionInformation(DBCoreModel):
    for_life: bool
    expiration_date: datetime
    plan_name: str
