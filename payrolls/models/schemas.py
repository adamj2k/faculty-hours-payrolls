from decimal import Decimal

from pydantic import BaseModel, Field


class Wages(BaseModel):
    id: int
    teacher_id: int
    teacher_name: str
    wage: float

    class Config:
        orm_mode = True


class MonthPayrolls(BaseModel):
    id: int
    teacher_id: int
    teacher_name: str
    year: int = Field(ge=2023)
    month: int = Field(ge=1, le=12)
    month_hours: int
    month_salary: Decimal = Field(decimal_places=2)


class MonthPayrollsResponse(BaseModel):
    id: int
    teacher_id: int
    teacher_name: str
    year: int = Field(ge=2023)
    month: int = Field(ge=1, le=12)
    month_hours: int
    month_salary: Decimal = Field(decimal_places=2)


class MonthPayrollsRequest(BaseModel):
    year: int = Field(ge=2023)
    month: int = Field(ge=1, le=12)
