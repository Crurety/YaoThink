
import asyncio
import os
import sys
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

# Add backend to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.core.database import DATABASE_URL, init_db

# Default credentials from database.py if standard env var logic matches
# We need to connect to 'postgres' db to create 'yaothink'
# Parse DATABASE_URL to replace db name
# Assuming format: postgresql+asyncpg://user:pass@host:port/dbname

async def create_database():
    hosts_to_try = []
    
    # Extract host from URL to decide what to try
    # Assumes standard format
    if "@" in DATABASE_URL:
        # postgresql+asyncpg://user:pass@host:port/dbname
        prefix, suffix = DATABASE_URL.split("@")
        host_port_db = suffix
    else:
         # Fallback
         host_port_db = "localhost:5432/yaothink"

    # We want to connect to 'postgres' db
    # We will try forcing host
    
    urls_to_try = [
        DATABASE_URL.replace("/yaothink", "/postgres"),
        DATABASE_URL.replace("/yaothink", "/postgres").replace("localhost", "127.0.0.1"),
        DATABASE_URL.replace("/yaothink", "/postgres").replace("localhost", "[::1]")
    ]

    for url in urls_to_try:
        print(f"Attempting connection to {url} ...")
        try:
            engine = create_async_engine(url, isolation_level="AUTOCOMMIT")
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
            
            await engine.dispose()
            return # Success
        except Exception as e:
            print(f"Failed to connect to {url}: {e}")
            await engine.dispose()
            
    print("Could not connect to any Postgres instance.")
    raise Exception("Database creation failed.")

async def main():
    try:
        await create_database()
        print("Initializing tables...")
        # Now init tables in the new db
        await init_db()
        print("Tables initialized successfully.")
    except Exception as e:
        print(f"Error during setup: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
