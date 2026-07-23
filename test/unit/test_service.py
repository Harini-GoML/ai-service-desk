import pytest

from app.models.ticket import Ticket
from app.schemas.ticket import CreateTicketRequest, UpdateTicketRequest
from app.exceptions.ticket_exceptions import TicketNotFoundError,TicketClosedError

@pytest.mark.asyncio
async def test_create_ticket(service, repo):
    request = CreateTicketRequest(
        title="Printer",
        priority="high",
    )
    repo.create.return_value = {
        "title": "Printer",
        "priority": "high",
    }
    ticket = await service.create_ticket(request)
    assert ticket["title"] == "Printer"
    repo.create.assert_awaited_once_with(request)

@pytest.mark.asyncio
async def test_get_ticket(service, repo):
    repo.get_by_id.return_value = {
        "id": 1,
        "title": "Printer"
    }
    ticket = await service.get_ticket(1)
    assert ticket["id"] == 1
    repo.get_by_id.assert_awaited_once_with(1)

@pytest.mark.asyncio
async def test_delete_ticket(service, repo):
    ticket = {
        "id": 1
    }
    repo.get_by_id.return_value = ticket
    await service.delete_ticket(1)
    repo.delete.assert_awaited_once_with(ticket)

@pytest.mark.asyncio
async def test_delete_ticket_not_found(service, repo):
    repo.get_by_id.return_value = None
    with pytest.raises(TicketNotFoundError):
        await service.delete_ticket(100)

@pytest.mark.asyncio
async def test_closed_ticket_cannot_be_reopened(service, repo):
    ticket = type("Ticket",(),{"status": "closed"})()
    repo.get_by_id.return_value = ticket
    request = UpdateTicketRequest(
        status="open"
    )
    with pytest.raises(TicketClosedError):
        await service.update_ticket(1,request)

@pytest.mark.asyncio
async def test_update_empty_payload(service, repo):
    ticket = Ticket(
      title="Printer",
      priority="High",
      status="open"
  )
    repo.get_by_id.return_value = ticket
    request = UpdateTicketRequest()
    repo.update.return_value = ticket
    result = await service.update_ticket(1,request)
    assert result == ticket