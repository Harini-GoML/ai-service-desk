import pytest
from app.schemas.ticket import CreateTicketRequest


class DummyTicket:
    pass


@pytest.mark.asyncio
async def test_repository_create(db,repo):
    payload = CreateTicketRequest(
        title= "Printer",
        priority= "high"
    )
    await repo.create(payload)
    db.add.assert_called_once()
    db.flush.assert_awaited_once()
    db.refresh.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_by_id(db, repo):
    ticket = DummyTicket()
    db.get.return_value = ticket
    result = await repo.get_by_id(1)
    assert result == ticket

@pytest.mark.asyncio
async def test_delete_ticket(db,repo):
    ticket = DummyTicket()
    await repo.delete(ticket)
    db.delete.assert_awaited_once()
    db.flush.assert_awaited_once()

@pytest.mark.asyncio
async def test_update_ticket(db,repo):
    ticket = DummyTicket()
    ticket.title = "Old"
    class Payload:
        def model_dump(self, exclude_unset=True):
            return {
                "title": "New"
            }
    await repo.update(ticket, Payload())
    assert ticket.title == "New"
    db.flush.assert_awaited_once()
    db.refresh.assert_awaited_once()