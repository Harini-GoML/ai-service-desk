from uuid import UUID
from app.exceptions.ticket_exceptions import TicketNotFoundError,TicketClosedError
from app.repositories.ticket_repository import TicketRepository
from app.schemas.ticket import CreateTicketRequest,UpdateTicketRequest

class TicketService:
    def __init__(self, repo: TicketRepository):
        self.repo = repo

    async def create_ticket(self,payload: CreateTicketRequest):
        return await self.repo.create(payload)
    
    async def get_ticket(self,ticket_id: UUID):
        return await self.repo.get_by_id(ticket_id) 
    
    async def get_all_tickets(self,id=None,status=None,priority=None):
        return await self.repo.get_all(id,status,priority)
    
    async def update_ticket(self,ticket_id: UUID,payload: UpdateTicketRequest):
        ticket = await self.repo.get_by_id(ticket_id)
        if ticket is None:
            raise TicketNotFoundError()
        if (ticket.status == "closed"and payload.status == "open"):
            raise TicketClosedError()
        return await self.repo.update(ticket,payload)
    
    async def delete_ticket(self,ticket_id: UUID):
        ticket = await self.repo.get_by_id(ticket_id)
        if ticket is None:
            raise TicketNotFoundError()
        await self.repo.delete(ticket)
        return {
            "message": "Ticket deleted successfully"
        }
