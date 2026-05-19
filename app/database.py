from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.config import settings # Import the settings object

# Pull the URL straight from the settings object itself
DATABASE_URL = settings.DATABASE_URL

# Setup the engine code
engine = create_async_engine(DATABASE_URL, echo=True)

# Create the session factory to generate individidual database sessions 
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False, # Faster performance
)

# Injectable Database Session
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try: 
            yield session
        finally:
            await session.close()