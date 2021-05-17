from pydantic import BaseModel

class QuestionEmail(BaseModel):
    user_email: str
    email_body: str

class EmailResponse(BaseModel):
    status_detail: str