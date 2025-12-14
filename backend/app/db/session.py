from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings

# Database engine
# Use SQLite for development/testing if PostgreSQL is not available
try:
    database_url = settings.DATABASE_URL
    # Replace postgresql with sqlite for local development
    if database_url.startswith("postgresql"):
        database_url = "sqlite:///./forensic_test.db"
    
    engine = create_engine(
        database_url,
        pool_pre_ping=True,
        connect_args={"check_same_thread": False} if database_url.startswith("sqlite") else {},
    )
except Exception:
    # Fallback to SQLite
    engine = create_engine(
        "sqlite:///./forensic_test.db",
        pool_pre_ping=True,
        connect_args={"check_same_thread": False}
    )

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
