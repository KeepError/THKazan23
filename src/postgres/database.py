from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy_utils import database_exists, create_database

from src.settings import settings

SQLALCHEMY_DATABASE_URL = settings.postgres_connection_string

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

Base = declarative_base()


# noinspection PyUnresolvedReferences
def setup_database():
    if not database_exists(engine.url):
        create_database(engine.url)

    from .models import raw_log, category, log_info, error, error_notification

    Base.metadata.create_all(bind=engine)


def get_session() -> Iterator[Session]:
    session: Session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@contextmanager
def session_ctx() -> Iterator[Session]:
    session: Session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
