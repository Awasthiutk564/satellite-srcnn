import asyncio
from app.db.session import engine
from sqlalchemy import text

async def test_db():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("Database connected successfully:", result.fetchone())
    except Exception as e:
        print("Database connection failed:", e)

if __name__ == "__main__":
    import asyncio
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("Database connected successfully:", result.fetchone())
    except Exception as e:
        print("Database connection failed:", e)
