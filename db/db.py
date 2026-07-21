"""SQLAlchemy session factory and owned-table bootstrap."""

import os
from contextlib import contextmanager
from typing import Any

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from db.models.base import Base
from db.models import owned  # noqa: F401 — side-effect: register owned models when added

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = None
SessionLocal = None

if DATABASE_URL:
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def get_db():
    """Yield a request-scoped session; always closes on exit."""
    if SessionLocal is None:
        raise RuntimeError("DATABASE_URL environment variable is required")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_owned_tables(bind: Any | None = None) -> None:
    """Create only tables owned by this repo — never upstream read mirrors."""
    if not owned.OWNED_MODELS:
        return
    target = bind or engine
    if target is None:
        raise RuntimeError("DATABASE_URL environment variable is required")
    tables = [model.__table__ for model in owned.OWNED_MODELS]
    Base.metadata.create_all(target, tables=tables)


def ensure_owned_tables(session: Session) -> None:
    """Create owned tables on the session's bind (e.g. at CLI startup)."""
    create_owned_tables(session.get_bind())
