from pydantic import BaseModel


class AuthService(BaseModel):
    def dump():
        return False
