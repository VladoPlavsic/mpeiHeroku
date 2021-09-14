from typing import Optional
from app.models.core import BaseModel

class TeamMemberBaseModel(BaseModel):
    order: int
    role: str
    name: str
    profession: str
    description: Optional[str]
    object_key: str

class PostTeamMemberModel(TeamMemberBaseModel):
    pass

class CreateTeamMemberModel(TeamMemberBaseModel):
    photo_link: str

class TeamMemberInDBModel(TeamMemberBaseModel):
    id: int
    photo_link: str

class UpdateTeamMemberModel(BaseModel):
    id: int
    photo_link: Optional[str]
    object_key: Optional[str]
    order: Optional[int]
    role: Optional[str]
    name: Optional[str]
    profession: Optional[str]
    description: Optional[str]

# about
class AboutProjectBaseModel(BaseModel):
    order: int
    html: str

class PostAboutProjectModel(AboutProjectBaseModel):
    pass

class CreateAboutProjectModel(AboutProjectBaseModel):
    pass

class AboutProjectInDBModel(AboutProjectBaseModel):
    pass

class UpdateAboutProjectModel(BaseModel):
    id: int
    order: Optional[int]
    html: Optional[str]

# contacts
class ContactsBaseModel(BaseModel):
    order: int
    html: str

class PostContactsModel(ContactsBaseModel):
    pass

class CreateContactsModel(ContactsBaseModel):
    pass

class ContactsInDBModel(ContactsBaseModel):
    pass

class UpdateContactsModel(BaseModel):
    id: int
    order: Optional[int]
    html: Optional[str]
