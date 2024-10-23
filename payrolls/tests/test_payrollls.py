from payrolls.models.models import MonthPayrolls
from payrolls.models.schemas import MonthPayrollsResponse


def test_get_month_payrolls_success(test_client, db_session):
    payroll_data = MonthPayrolls(
        id=1, year=2024, month=1, teacher_id=1, teacher_name="John Doe", month_hours=100, month_salary=4000.0
    )
    db_session.add(payroll_data)
    db_session.commit()

    response = test_client.get(f"/month-payrolls/2024/1")
    assert response.status_code == 200
    assert response.json() == MonthPayrollsResponse(**payroll_data.__dict__).model_dump()


def test_get_month_payrolls_not_found(test_client, db_session):
    # Test the function with non-existent year and month
    response = test_client.get("/month-payrolls/2024/13")
    assert response.status_code == 404
    assert response.json()["detail"] == "Payrolls for that 2024 and 13 not found."


def test_get_month_payrolls_invalid_year(test_client, db_session):
    # Test the function with invalid year
    response = test_client.get("/month-payrolls/-1/1")
    assert response.status_code == 404
    assert response.json()["detail"] == "Payrolls for that -1 and 1 not found."


def test_get_month_payrolls_invalid_month(test_client, db_session):
    # Test the function with invalid month
    response = test_client.get("/month-payrolls/2024/-1")
    assert response.status_code == 404
    assert response.json()["detail"] == "Payrolls for that 2024 and -1 not found."
