from pydantic import BaseModel, EmailStr

class CreateUserModel(BaseModel):
    email: EmailStr
    password: str