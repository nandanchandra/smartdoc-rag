from pydantic import BaseModel


class BaseResponseModel(BaseModel):
    message: str
