from pydantic import BaseModel, EmailStr, ConfigDict


class UserPublic(BaseModel):
    id: int
    name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)
