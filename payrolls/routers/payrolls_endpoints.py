from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from payrolls.logic.payrolls import (
    create_payrolls_for_month_of_year,
    save_payrolls_to_database,
)
from payrolls.models.database import get_db
from payrolls.models.schemas import (
    MonthPayrolls,
    MonthPayrollsRequest,
    MonthPayrollsResponse,
)

router = APIRouter()


@router.get("/month-payrolls/{year}/{month}", response_model=MonthPayrollsResponse)
async def get_month_payrolls(year: int, month: int, db: Session = Depends(get_db)):
    month_payrolls = db.query(MonthPayrolls).filter(MonthPayrolls.year == year, MonthPayrolls.month == month).first()
    if month_payrolls == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Payrolls for that {year} and {month} not found."
        )
    return month_payrolls


@router.post("/month-payrolls/create", response_model=MonthPayrollsRequest)
async def create_month_payrolls(payrolls_data: MonthPayrollsRequest, db: Session = Depends(get_db)):
    new_payrolls = create_payrolls_for_month_of_year(payrolls_data.year, payrolls_data.month)
    save_payrolls_to_database(new_payrolls)
    return new_payrolls
