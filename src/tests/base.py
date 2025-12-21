import unittest

from db import DB


class BaseTestCase(unittest.TestCase):
    """Base test case that sets up an in-memory SQLite DB and repository."""

    def setUp(self):
        self.db = DB(memory=True)
        self.db.create_metadata()
