"""Utility classes for database connection and session management and model definitions."""

from contextlib import contextmanager
from typing import ContextManager

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, SessionTransaction, sessionmaker


class Base(DeclarativeBase):
    pass


class DB:
    """Wrapper for SQLAlchemy ORM sessionmaker with a configurable database path.

    ### Parameters
      #### db_path
      A file path to the database file.
      #### memory
      If True, an in-memory SQLite database is used.
    """

    def __init__(self, db_path: str, memory: bool = False) -> None:
        if memory:
            db_url = "sqlite+pysqlite:///:memory:"
        else:
            db_url = f"sqlite+pysqlite:///{db_path}"

        self._engine = create_engine(db_url, echo=False)
        self._sessionmaker = sessionmaker(bind=self._engine)

    def session(self) -> Session:
        session = self._sessionmaker()
        session.expire_on_commit = False
        return session

    def begin(self) -> ContextManager[Session]:
        """Wrapper around sessionmaker's session.begin() with expire_on_commit applied."""

        @contextmanager
        def _begin():
            session = self._sessionmaker()
            session.expire_on_commit = False
            try:
                with session.begin():
                    yield session
            finally:
                session.close()

        return _begin()

    def create_metadata(self) -> None:
        """Create all tables defined in the models."""
        Base.metadata.create_all(bind=self._engine)
