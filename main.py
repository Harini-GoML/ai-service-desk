# def main():
#     print("Hello from ai-service-desk!")


# if __name__ == "__main__":
#     main()
# from app.models.ticket import Ticket
# print(Ticket.__tablename__)

import asyncio
from sqlalchemy import text

from app.core.database import AsyncSessionLocal


async def test():
    async with AsyncSessionLocal() as session:
        result = await session.execute(text("SELECT version();"))
        print(result.scalar())


asyncio.run(test())