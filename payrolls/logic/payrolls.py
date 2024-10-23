import pandas as pd

from payrolls.models.database import SessionLocal
from payrolls.models.models import MonthPayrolls
from payrolls.routers.get_data import get_personal_reports_list


def get_wages_for_teachers(teacher_list: list) -> pd.DataFrame:
    with SessionLocal() as db:
        all_wages = pd.read_sql("wages", db.bind)
        if all_wages.empty:
            return None  # TODO raise exception
    teachers_wages = all_wages.loc[all_wages["teacher_name"].isin(teacher_list)]
    return teachers_wages


def get_data_to_count_payrolls(personal_report: dict, wages: pd.DataFrame) -> pd.DataFrame:
    """
    Function to get data ready for counting payrolls. Join data from personal report and wages.

    Args:
        personal_report (pd.DataFrame): A DataFrame containing the personal report data for each teacher.
        wages (pd.DataFrame): A DataFrame containing the wages data for teachers.

    Returns:
        pd.DataFrame: A DataFrame containing the ready data to count payrolls.
    """
    df_personal_report = pd.DataFrame.from_dict(personal_report["personal_workload_report"])
    data = pd.merge(df_personal_report, wages, left_on="teacher", right_on="teacher_name")
    return data


def count_payrolls_for_month_of_year(data: pd.DataFrame, year: int, month: int) -> pd.DataFrame:
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
    data["month_hours"] = data["sum_hours"] / 12
    data["month_salary"] = data["month_hours"] * data["wage"]
    data.drop(
        columns=[
            "_id",
            "teacher",
            "hours_semester1",
            "hours_semester2",
            "sum_hours",
            "difference_pensum_sum_hours",
            "id",
            "wage",
            "pensum",
        ],
        inplace=True,
    )
    return data


def save_payrolls_to_database(payrolls: pd.DataFrame, db) -> None:
    """
    Save payrolls to database.

    Args:
        payrolls (pd.DataFrame): DataFrame containing payrolls data.

    Returns:
        None
    """
    payrolls_dict = payrolls.to_dict(orient="records")
    payrolls_to_save = [MonthPayrolls(**payroll) for payroll in payrolls_dict]
    db.add_all(payrolls_to_save)
    db.commit()


def check_payroll_in_database(year: int, month: int) -> bool:
    """
    Check if payroll for given year and month exists in database.

    Args:
        year (int): Year of payroll.
        month (int): Month of payroll.

    Returns:
        bool: True if payroll exists, False otherwise.
    """
    db = SessionLocal()
    month_payrolls = db.query(MonthPayrolls).filter(MonthPayrolls.year == year, MonthPayrolls.month == month).first()
    return month_payrolls is not None


def get_list_of_teachers_from_personal_reports_list(personal_report_for_all_teachers: list) -> list:
    """
    Get list of teachers from personal report list.
    """
    list_of_teachers = []
    for teacher in personal_report_for_all_teachers["personal_workload_report"]:
        list_of_teachers.append(teacher["teacher"])
    return list_of_teachers


def get_wages_for_all_teachers(list_of_teachers: list) -> pd.DataFrame:
    """
    Get list of teachers from personal report list.
    """
    teachers_wages = get_wages_for_teachers(list_of_teachers)
    return teachers_wages


def create_payrolls_for_month_of_year(year: int, month: int) -> pd.DataFrame:
    """ """
    if check_payroll_in_database(year, month) == True:
        raise Exception  # TODO make custom exception
    personal_report_for_all_teachers = get_personal_reports_list()
    list_of_teachers = get_list_of_teachers_from_personal_reports_list(personal_report_for_all_teachers)
    wages_for_all_teachers = get_wages_for_all_teachers(list_of_teachers)
    data_from_personal_report = get_data_to_count_payrolls(personal_report_for_all_teachers, wages_for_all_teachers)
    payrolls = count_payrolls_for_month_of_year(data=data_from_personal_report, year=year, month=month)
    return payrolls
