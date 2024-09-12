import pandas as pd
from models.database import get_db
from models.models import MonthPayrolls


def get_data_to_count_payrolls(personal_report: pd.DataFrame, wages: pd.DataFrame) -> pd.DataFrame:
    """
    Function to get data ready for counting payrolls. Join data from personal report and wages.

    Args:
        personal_report (pd.DataFrame): A DataFrame containing the personal report data for each teacher.
        wages (pd.DataFrame): A DataFrame containing the wages data for teachers.

    Returns:
        pd.DataFrame: A DataFrame containing the ready data to count payrolls.
    """
    data = pd.merge(personal_report, wages, on_left="id", on_right="teacher_id")
    return data


def count_payrolls(data: pd.DataFrame, year: int, month: int) -> pd.DataFrame:
    """
    Function to count payrolls.
    For month payroll we divide hours by 5 months in semester.

    Args:
        data (pd.DataFrame): A DataFrame containing the data to count payrolls.
        year (int): The year to count payrolls.
        month (int): The month to count payrolls.

    Returns:
        pd.DataFrame: A DataFrame containing the counted payrolls.
    """
    data["year"] = year
    data["month"] = month
    data["month_hours"] = data["hours"] / 5
    data["month_payroll"] = data["month_hours"] * data["wage"]
    return data


def save_payrolls_to_database(payrolls: pd.DataFrame) -> None:
    """
    Save payrolls to database.

    Args:
        payrolls (pd.DataFrame): DataFrame containing payrolls data.

    Returns:
        None
    """
    db = get_db()
    payrolls_to_save = MonthPayrolls(**payrolls.model_dump())
    db.add(payrolls_to_save)
    db.commit()
    db.refresh(payrolls_to_save)
