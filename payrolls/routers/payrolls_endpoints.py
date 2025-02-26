from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from payrolls.logic.payrolls import (
    create_payrolls_for_month_of_year,
    save_payrolls_to_database,
)
from payrolls.models import models
from payrolls.models.database import get_db
from payrolls.models.schemas import MonthPayrollsRequest, MonthPayrollsResponse, Wages

router = APIRouter()


@router.post("/wage", status_code=status.HTTP_201_CREATED, response_model=Wages)
async def create_wage(wage_data: Wages, db: Session = Depends(get_db)):
    new_wage = models.Wages(**wage_data.model_dump())
    db.add(new_wage)
    db.commit()
    db.refresh(new_wage)
    return new_wage


@router.get("/wage/{wage_id}", response_model=Wages)
async def get_wage(wage_id: int, db: Session = Depends(get_db)):
    wage = db.query(models.Wages).filter(models.Wages.id == wage_id).first()
    if wage is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Wage with id {wage_id} not found.")
    return wage


@router.get("/wages", response_model=list[Wages])
async def get_all_wages(db: Session = Depends(get_db)):
    all_wages = db.query(models.Wages).all()
    if all_wages is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Wages not found.")
    return all_wages


@router.get("/month-payrolls/{year}/{month}", response_model=MonthPayrollsResponse)
async def get_month_payrolls(year: int, month: int, db: Session = Depends(get_db)):
    month_payrolls = (
        db.query(models.MonthPayrolls)
        .filter(models.MonthPayrolls.year == year, models.MonthPayrolls.month == month)
        .first()
    )
    if month_payrolls is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Payrolls for that {year} and {month} not found."
        )
    return month_payrolls


@router.post("/month-payrolls/create")
async def create_month_payrolls(payrolls_data: MonthPayrollsRequest, db: Session = Depends(get_db)):
    new_payrolls = create_payrolls_for_month_of_year(payrolls_data.year, payrolls_data.month)
    save_payrolls_to_database(new_payrolls, db)
    return_payrolls = new_payrolls.to_dict(orient="records")
    return return_payrolls
