from importlib import import_module
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Database location
BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "chatbot.db"

DATABASE_URL = f"sqlite:///{DATABASE_PATH.as_posix()}"


# Database engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)


# Database sessions
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


# Base class for database models
class Base(DeclarativeBase):
    pass

def create_tables() -> None:
    # Load models so SQLAlchemy registers their tables.
    import_module("database.models")

    Base.metadata.create_all(bind=engine)
