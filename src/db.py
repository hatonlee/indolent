"""creates a session for the database"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Base(DeclarativeBase):
    pass


DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")
DB_URL = f"sqlite:///{DB_PATH}"


engine = create_engine(DB_URL, echo=False)
session = sessionmaker(engine)
