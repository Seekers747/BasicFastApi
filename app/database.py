from sqlalchemy import create_engine # type: ignore[reportMissingImports]
from sqlalchemy.orm import sessionmaker, Session # type: ignore[reportMissingImports]
from contextlib import contextmanager
from .models import Base  # pyright: ignore[reportMissingImports]

# SQLite database URL
DATABASE_URL = "sqlite:///./app.db"

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Needed for SQLite
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Create all tables in the database."""
    Base.metadata.create_all(bind=engine)

@contextmanager
def get_db():
    """Dependency for getting database sessions."""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()