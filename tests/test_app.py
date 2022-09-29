from fastapi.testclient import TestClient
from app.main import app


def test_get_restourant():
    with TestClient(app) as client:
        response = client.get("/restaurants/749beb15-6228-40be-beb3-5584badfa364")

    assert response.status_code == 200
    assert response.json() == {
        "name": "Fafa's Sokos",
        "description": "Delicious pitas, salads and more",
        "id": "749beb15-6228-40be-beb3-5584badfa364",
        "location": {
            "city": "Helsinki",
            "coordinates": {"lon": 24.93900239467621, "lat": 60.1707249837842},
        },
    }


def test_get_restaurant_returns_not_found_when_not_legit_id():
    with TestClient(app) as client:
        response = client.get("/restaurants/this-should-not-exist")

    assert response.status_code == 404
    assert {"detail": "Restaurant not found"} == response.json()
