import uuid
import pytest


@pytest.mark.asyncio
async def test_get_all_tickets(client):
    response = await client.get("/tickets/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_filter_by_priority(client):
    await client.post(
        "/tickets/",
        json={
            "title": "Printer Issue",
            "description": "Printer not working",
            "priority": "high",
        },
    )

    response = await client.get("/tickets/?priority=high")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)

    for ticket in data:
        assert ticket["priority"] == "high"


@pytest.mark.asyncio
async def test_filter_by_status(client):
    await client.post(
        "/tickets/",
        json={
            "title": "Login Issue",
            "description": "Unable to login",
        },
    )

    response = await client.get("/tickets/?status=open")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)

    for ticket in data:
        assert ticket["status"] == "open"


@pytest.mark.asyncio
async def test_filter_no_matching_records(client):
    response = await client.get("/tickets/?status=resolved")

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_ticket_by_id(client):
    create_response = await client.post(
        "/tickets/",
        json={
            "title": "Keyboard Issue",
            "description": "Keyboard keys are not working",
            "priority": "high",
        },
    )

    assert create_response.status_code == 201

    ticket_id = create_response.json()["id"]

    response = await client.get(f"/tickets/{ticket_id}")

    assert response.status_code == 200

    data = response.json()
    assert data["id"] == ticket_id
    assert data["title"] == "Keyboard Issue"
    assert data["priority"] == "high"


@pytest.mark.asyncio
async def test_get_non_existing_ticket(client):
    fake_id = str(uuid.uuid4())

    response = await client.get(f"/tickets/{fake_id}")

    assert response.status_code == 404