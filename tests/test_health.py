
import pytest

from app import create_app
from app.extensions import db


@pytest.fixture
def client():

    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })

    with app.app_context():
        db.create_all()

        yield app.test_client()

        db.session.remove()
        db.drop_all()


def test_health_check(client):

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "healthy"
    assert response.json["service"] == "ticket-tracker-api"


def test_create_ticket(client):

    response = client.post(
        "/tickets",
        json={
            "title": "Outlook not working",
            "description": "Unable to open Outlook application",
            "priority": "P1"
        }
    )

    assert response.status_code == 201
    assert response.json["priority"] == "P1"
    assert response.json["status"] == "Open"


def test_get_tickets(client):

    client.post(
        "/tickets",
        json={
            "title": "VPN issue",
            "description": "VPN connection failed",
            "priority": "P2"
        }
    )

    response = client.get("/tickets")

    assert response.status_code == 200
    assert len(response.json) == 1


def test_invalid_priority(client):

    response = client.post(
        "/tickets",
        json={
            "title": "Test issue",
            "description": "Testing invalid priority",
            "priority": "P5"
        }
    )

    assert response.status_code == 400


def test_update_ticket(client):

    created = client.post(
        "/tickets",
        json={
            "title": "Printer issue",
            "description": "Printer not responding",
            "priority": "P2"
        }
    )

    ticket_id = created.json["id"]

    response = client.put(
        f"/tickets/{ticket_id}",
        json={"status": "Resolved"}
    )

    assert response.status_code == 200
    assert response.json["status"] == "Resolved"


def test_delete_ticket(client):

    created = client.post(
        "/tickets",
        json={
            "title": "Keyboard issue",
            "description": "Keyboard not working",
            "priority": "P3"
        }
    )

    ticket_id = created.json["id"]

    response = client.delete(f"/tickets/{ticket_id}")

    assert response.status_code == 200

    missing = client.get(f"/tickets/{ticket_id}")

    assert missing.status_code == 404
