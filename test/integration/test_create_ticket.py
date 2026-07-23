import pytest


@pytest.mark.asyncio
async def test_create_ticket_success(client):
    payload = {
        "title": "Printer not working",
        "description": "The office printer is not printing documents.",
        "priority": "High",
        "assignee_email": "support@example.com",
    }

    response = await client.post(
        "/tickets/",
        json=payload,
    )

    assert response.status_code == 201

    data = response.json()
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
    assert data["priority"] == payload["priority"]
    assert data["assignee_email"] == payload["assignee_email"]
    assert "id" in data
    assert "status" in data
    assert "created_at" in data


@pytest.mark.asyncio
async def test_create_ticket_without_priority(client):
    payload = {
        "title": "Cannot login",
        "description": "Employee is unable to login to the portal.",
    }

    response = await client.post(
        "/tickets/",
        json=payload,
    )

    assert response.status_code == 201

    data = response.json()
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
    assert data["priority"] == "Medium"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "priority",
    [
        "urgent",
        "critical",
        "LOW",
        "123",
    ],
)
async def test_create_ticket_invalid_priority(client, priority):
    payload = {
        "title": "Printer Issue",
        "description": "Printer is offline.",
        "priority": priority,
    }

    response = await client.post(
        "/tickets/",
        json=payload,
    )

    assert response.status_code == 422


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload",
    [
        {
            "description": "Missing title",
        },
        {
            "title": "Missing description",
        },
        {},
    ],
)
async def test_create_ticket_missing_required_fields(client, payload):
    response = await client.post(
        "/tickets/",
        json=payload,
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_ticket_empty_title(client):
    payload = {
        "title": "",
        "description": "Printer issue",
    }

    response = await client.post(
        "/tickets/",
        json=payload,
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_ticket_title_with_spaces(client):
    payload = {
        "title": "    ",
        "description": "Printer issue",
    }

    response = await client.post(
        "/tickets/",
        json=payload,
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_ticket_title_too_long(client):
    payload = {
        "title": "A" * 201,
        "description": "Printer issue",
    }

    response = await client.post(
        "/tickets/",
        json=payload,
    )

    assert response.status_code == 422