"""Utility classes for database connection and session management and model definitions."""

from contextlib import contextmanager
from typing import ContextManager

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


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

    def __init__(self, db_path: str | None = None, memory: bool = False) -> None:
        if memory:
            db_url = "sqlite+pysqlite:///:memory:"
        elif db_path:
            db_url = f"sqlite+pysqlite:///{db_path}"
        else:
            raise ValueError(
                "Either `db_path` must be provided or `memory` must be `True`."
            )

        self._engine = create_engine(db_url, echo=False)
        self._sessionmaker = sessionmaker(bind=self._engine)

    def session(self) -> Session:
        """Get a new session with expire_on_commit set to False."""
        session = self._sessionmaker()
        session.expire_on_commit = False
        return session

    def begin(self) -> ContextManager[Session]:
        """Get a new context manager with a session with expire_on_commit set to False."""

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
