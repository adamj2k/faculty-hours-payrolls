from typing import List

from pydantic import BaseModel, EmailStr, Field, computed_field


class temp(BaseModel):
    id: int
    name: str
    last_name: str
    email: EmailStr
