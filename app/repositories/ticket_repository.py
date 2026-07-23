from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.ticket import Ticket

class TicketRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, payload):
        ticket = Ticket(
            **payload.model_dump()
        )
        self.db.add(ticket)
        await self.db.flush()
        await self.db.refresh(ticket)
        return ticket
    
    async def get_by_id(self,ticket_id: UUID):
        return await self.db.get(
            Ticket,
            ticket_id
        )
    
    async def get_all(self,id: Optional[UUID]=None,status: Optional[str] = None,priority: Optional[str] = None):
        query = select(Ticket)
        if id:
            query = query.where(
                Ticket.id == id
            )
        if status:
            query = query.where(
                Ticket.status == status
            )
        if priority:
            query = query.where(
                Ticket.priority == priority
            )
        query = query.order_by(
            Ticket.created_at.desc()
        )
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def update(self,ticket,payload):
        for field, value in payload.model_dump(exclude_unset=True).items():#update dynamically
            setattr(ticket,field,value)
        await self.db.flush()
        await self.db.refresh(ticket)
        return ticket
    
    async def delete(self,ticket):
        await self.db.delete(ticket)
        await self.db.flush()