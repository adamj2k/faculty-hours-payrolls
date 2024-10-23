from payrolls.models.models import Wages


def test_get_wage_existing_id(test_client, db_session):
    # Test retrieving the wage with the existing ID
    wage = Wages(id=1, teacher_id=1, teacher_name="John Doe", wage=100.0)
    db_session.add(wage)
    db_session.commit()

    response = test_client.get(f"/wage/{wage.id}")
    assert response.status_code == 200
    assert response.json() == {
        "id": wage.id,
        "teacher_id": wage.teacher_id,
        "teacher_name": wage.teacher_name,
        "wage": wage.wage,
    }


def test_get_wage_non_existent_id(test_client):
    # Test retrieving a wage with a non-existent ID
    response = test_client.get("/wage/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Wage with id 999 not found."}


def test_get_wage_invalid_id(test_client):
    # Test retrieving a wage with an invalid ID (non-integer)
    response = test_client.get("/wage/abc")
    assert response.status_code == 422
    assert "value is not a valid integer" in response.json()["detail"][0]["msg"]
