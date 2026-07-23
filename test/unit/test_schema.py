from pydantic import ValidationError
import pytest
from app.schemas.ticket import CreateTicketRequest,UpdateTicketRequest

def test_create_ticket_valid():
    ticket = CreateTicketRequest(
        title="Printer not working",
        priority="high"
    )
    assert ticket.title == "Printer not working"
    assert ticket.priority == "high"

def test_priority_default():
    ticket = CreateTicketRequest(
        title="Printer issue"
    )
    assert ticket.priority == "medium"

def test_empty_title():
    with pytest.raises(ValidationError):
        CreateTicketRequest(
            title="",
            priority="High"
        )

def test_invalid_priority():
    with pytest.raises(ValidationError):
        CreateTicketRequest(
            title="Printer",
            priority="Urgent"
        )

def test_minimum_length_title():
    ticket = CreateTicketRequest(
        title="ABC"
    )
    assert ticket.title == "ABC"

def test_maximum_length_title():
    ticket = CreateTicketRequest(
        title="A" * 200
    )
    assert len(ticket.title) == 200

def test_title_too_long():
    with pytest.raises(ValidationError):
        CreateTicketRequest(
            title="A" * 201
        )

def test_update_status():
    ticket = UpdateTicketRequest(
        status="resolved"
    )
    assert ticket.status == "resolved"

def test_invalid_status():
    with pytest.raises(ValidationError):
        UpdateTicketRequest(
            status="completed"
        )