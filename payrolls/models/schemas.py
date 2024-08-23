from pydantic import BaseModel, EmailStr


class temp(BaseModel):
    id: int
    name: str
    last_name: str
    email: EmailStr
