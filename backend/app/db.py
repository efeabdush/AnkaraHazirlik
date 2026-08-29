from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from .config import settings


connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(settings.database_url, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def ensure_schema() -> None:
    """Add columns introduced after the first local SQLite file was created."""
    if not settings.database_url.startswith("sqlite"):
        return
    with engine.begin() as conn:
        cols = {row[1] for row in conn.execute(text("PRAGMA table_info(tests)"))}
        if "glossary_json" not in cols:
            conn.execute(text("ALTER TABLE tests ADD COLUMN glossary_json TEXT DEFAULT '[]'"))
        if "content_json" not in cols:
            conn.execute(text("ALTER TABLE tests ADD COLUMN content_json TEXT DEFAULT '{}'"))
        if "instructions" not in cols:
            conn.execute(text("ALTER TABLE tests ADD COLUMN instructions TEXT DEFAULT ''"))


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
