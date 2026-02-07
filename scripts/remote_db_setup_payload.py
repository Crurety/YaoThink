
import asyncio
import os
import sys

# Add /app to sys.path since that's where the code lives in the container
sys.path.append("/app")

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from app.core.database import DATABASE_URL, init_db

# In the container, DATABASE_URL should be set correctly in env, 
# but let's double check or override if needed.
# Typically DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/yaothink

async def create_database_if_not_exists():
    print(f"Checking database using URL: {DATABASE_URL}")
    
    # We need to connect to 'postgres' db to manage databases
    # Assumes standard format: postgresql+asyncpg://user:pass@host:port/dbname
    if "/yaothink" in DATABASE_URL:
        postgres_url = DATABASE_URL.replace("/yaothink", "/postgres")
    else:
        # Fallback for safety, though env should be right
        postgres_url = "postgresql+asyncpg://postgres:postgres@db:5432/postgres"

    print(f"Connecting to {postgres_url} to check databases...")
    
    engine = create_async_engine(postgres_url, isolation_level="AUTOCOMMIT")
    
    try:
        async with engine.connect() as conn:
            # Check if database exists
            result = await conn.execute(text("SELECT 1 FROM pg_database WHERE datname = 'yaothink'"))
            exists = result.scalar()
            
            if not exists:
                print("Database 'yaothink' does not exist. Creating...")
                await conn.execute(text("CREATE DATABASE yaothink"))
                print("Database 'yaothink' created successfully.")
            else:
                print("Database 'yaothink' already exists.")
    except Exception as e:
        print(f"Error checking/creating database: {e}")
        raise
    finally:
        await engine.dispose()

async def main():
    try:
        await create_database_if_not_exists()
        
        # Now init tables in the yaothink db
        print("Initializing tables via app.core.database.init_db()...")
        await init_db()
        print("Tables initialized successfully.")
    except Exception as e:
        print(f"Remote setup failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
