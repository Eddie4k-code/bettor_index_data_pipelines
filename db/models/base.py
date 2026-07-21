"""SQLAlchemy declarative bases for owned vs upstream tables."""

from sqlalchemy.orm import declarative_base

Base = declarative_base()
UpstreamBase = declarative_base()
