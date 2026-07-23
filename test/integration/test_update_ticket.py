import uuid
import pytest


@pytest.mark.asyncio
async def test_update_ticket_title(client):
    create_response = await client.post(
        "/tickets/",
        json={
            "title": "Printer",
            "description": "Printer not working",
            "priority": "high",
        },
    )

    ticket_id = create_response.json()["id"]

    response = await client.patch(
        f"/tickets/{ticket_id}",
        json={
            "title": "Printer Updated",
        },
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Printer Updated"


@pytest.mark.asyncio
async def test_update_ticket_status(client):
    create_response = await client.post(
        "/tickets/",
        json={
            "title": "Laptop",
            "description": "Laptop not starting",
            "priority": "medium",
        },
    )

    ticket_id = create_response.json()["id"]

    response = await client.patch(
        f"/tickets/{ticket_id}",
        json={
            "status": "resolved",
        },
    )

    assert response.status_code == 200
    assert response.json()["status"] == "resolved"


@pytest.mark.asyncio
async def test_update_invalid_priority(client):
    create_response = await client.post(
        "/tickets/",
        json={
            "title": "Mouse",
            "description": "Mouse not working",
        },
    )

    ticket_id = create_response.json()["id"]

    response = await client.patch(
        f"/tickets/{ticket_id}",
        json={
            "priority": "urgent",
        },
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_non_existing_ticket(client):
    fake_id = str(uuid.uuid4())

    response = await client.patch(
        f"/tickets/{fake_id}",
        json={
            "title": "ABC",
        },
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_empty_body(client):
    create_response = await client.post(
        "/tickets/",
        json={
            "title": "Monitor",
            "description": "Monitor flickering",
        },
    )

    ticket_id = create_response.json()["id"]

    response = await client.patch(
        f"/tickets/{ticket_id}",
        json={},
    )

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_closed_ticket_cannot_reopen(client):
    create_response = await client.post(
        "/tickets/",
        json={
            "title": "CPU",
            "description": "CPU overheating",
        },
    )

    ticket_id = create_response.json()["id"]

    close_response = await client.patch(
        f"/tickets/{ticket_id}",
        json={
            "status": "closed",
        },
    )

    assert close_response.status_code == 200

    reopen_response = await client.patch(
        f"/tickets/{ticket_id}",
        json={
            "status": "open",
        },
    )

    assert reopen_response.status_code == 400