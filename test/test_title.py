import pytest
from pydantic import ValidationError

from app.schemas.ticket import CreateTicketRequest

def test_create_ticket_with_empty_title_returns_422(client):
    response = client.post(
        "/tickets",
        json={
            "title": 4,
        }
    )

    assert response.status_code == 422

def test_create_ticket_blank_title_validation():
    with pytest.raises(ValidationError) as exc_info:
        CreateTicketRequest(
            title="   ",
            priority="High"
        )

    assert "Title cannot be blank" in str(exc_info.value)