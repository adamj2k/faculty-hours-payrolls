from fastapi import requests
from sqlalchemy import ForeignKey  # noqa
from sqlalchemy import TIMESTAMP, Column, Double, Integer, String, text
from sqlalchemy.ext.declarative import declarative_base

from payrolls import settings
from payrolls.models.database import Base

Base = declarative_base()


class Wages(Base):
    __tablename__ = "wages"

    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer)
    teacher_name = Column(String(100))
    wage = Column(Double(10, 2))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

    def validate_teacher(self, teacher_id):
        request = requests.get(f"http://{settings.FH_APP_FACULTY_URL}/faculty/teacher/{teacher_id}")
        if request.status_code == 404:
            raise Exception("Teacher not found")
        else:
            return True


class MonthPayrolls(Base):
    __tablename__ = "summary"

    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer)
    teacher_name = Column(String(100))
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    month_hours = Column(Integer)
    month_salary = Column(Double(10, 2))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
