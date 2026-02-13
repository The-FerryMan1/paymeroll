from app.core.database import AsyncSessionLocal


async def getDB():
   async with AsyncSessionLocal() as session:
         yield session

