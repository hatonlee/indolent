import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db import Base


class BaseTestCase(unittest.TestCase):
    """Base test case that sets up an in-memory SQLite DB and repository."""

    def setUp(self):
        engine = create_engine("sqlite:///:memory:", echo=False)
        self.session = sessionmaker(engine, expire_on_commit=False)
        Base.metadata.create_all(bind=engine)
