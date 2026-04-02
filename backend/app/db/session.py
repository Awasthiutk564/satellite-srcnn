from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


connect_args = {"check_same_thread": False} if settings.SQLALCHEMY_DATABASE_URI.startswith("sqlite") else {}
engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, connect_args=connect_args, future=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
