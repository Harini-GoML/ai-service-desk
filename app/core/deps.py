from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.ticket_service import TicketService
from app.core.database import AsyncSessionLocal
from app.repositories.ticket_repository import TicketRepository

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        
def get_repo(db: AsyncSession = Depends(get_db)):
    return TicketRepository(db)

def get_service(repo: TicketRepository = Depends(get_repo)):
    return TicketService(repo)