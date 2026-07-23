import uuid
import pytest


@pytest.mark.asyncio
async def test_delete_ticket_success(client):
    payload = {
        "title": "Router issue",
        "description": "Router is not working",
        "priority": "High",
    }

    create_response = await client.post(
        "/tickets/",
        json=payload,
    )

    assert create_response.status_code == 201

    ticket_id = create_response.json()["id"]

    response = await client.delete(f"/tickets/{ticket_id}")

    assert response.status_code == 204


@pytest.mark.asyncio
async def test_deleted_ticket_not_found(client):
    payload = {
        "title": "Switch issue",
        "description": "Switch is not responding",
    }

    create_response = await client.post(
        "/tickets/",
        json=payload,
    )

    ticket_id = create_response.json()["id"]

    await client.delete(f"/tickets/{ticket_id}")

    response = await client.get(f"/tickets/{ticket_id}")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_non_existing_ticket(client):
    fake_id = str(uuid.uuid4())

    response = await client.delete(f"/tickets/{fake_id}")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_same_ticket_twice(client):
    payload = {
        "title": "WiFi issue",
        "description": "WiFi keeps disconnecting",
    }

    create_response = await client.post(
        "/tickets/",
        json=payload,
    )

    ticket_id = create_response.json()["id"]

    first_response = await client.delete(f"/tickets/{ticket_id}")
    assert first_response.status_code == 204

    second_response = await client.delete(f"/tickets/{ticket_id}")

    assert second_response.status_code == 404