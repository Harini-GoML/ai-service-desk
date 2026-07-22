from uuid import UUID
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from app.schemas.ticket import CreateTicketRequest,UpdateTicketRequest
from app.services.ticket_service import TicketService
from app.core.deps import get_service
from app.exceptions.ticket_exceptions import TicketNotFoundError,TicketClosedError

router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"],
)

@router.get("/")
async def get_tickets(
    id: UUID | None = None,
    status: str | None = None,
    priority: str | None = None,
    service: TicketService = Depends(get_service)
):
    return await service.get_all_tickets(id,status,priority)

@router.post("/")
async def create_ticket(
    payload: CreateTicketRequest,
    service: TicketService = Depends(get_service)
):
    return await service.create_ticket(payload)

@router.patch("/{ticket_id}")
async def update_ticket(
    ticket_id: UUID,
    payload: UpdateTicketRequest,
    service: TicketService = Depends(get_service)
):
    try:
        return await service.update_ticket(ticket_id, payload)
    
    except TicketNotFoundError:
        raise HTTPException(status_code=404,detail="Ticket not found")
    
    except TicketClosedError:
        raise HTTPException(status_code=400,detail="Closed tickets cannot be reopened")

@router.delete("/{ticket_id}")
async def delete_ticket(
    ticket_id: UUID,
    service: TicketService = Depends(get_service)
):
    try:
        return await service.delete_ticket(ticket_id)
    except TicketNotFoundError:
        raise HTTPException(status_code=404,detail="Ticket not found")