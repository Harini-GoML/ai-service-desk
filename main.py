import asyncio
from sqlalchemy import text

from app.core.database import AsyncSessionLocal


async def test():
    async with AsyncSessionLocal() as session:
        result = await session.execute(text("SELECT version();"))
        print(result.scalar())


asyncio.run(test())