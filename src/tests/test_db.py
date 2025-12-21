import unittest
from unittest.mock import patch

from sqlalchemy.orm import Session

from db import DB


class TestDB(unittest.TestCase):
    def setUp(self):
        self.db = DB(memory=True)
        self.db.create_metadata()

    def test_session(self):
        with self.db.session() as session:
            self.assertIsInstance(session, Session)

    def test_context_manager_session(self):
        with self.db.begin() as session:
            self.assertIsInstance(session, Session)

    def test_init_no_params(self):
        with self.assertRaises(ValueError):
            DB()

    @patch("db.sessionmaker")
    @patch("db.create_engine")
    def test_init_memory(self, mock_create_engine, mock_sessionmaker):
        DB(memory=True)
        mock_create_engine.assert_called_with("sqlite+pysqlite:///:memory:", echo=False)
        mock_sessionmaker.assert_called_with(bind=mock_create_engine.return_value)

    @patch("db.sessionmaker")
    @patch("db.create_engine")
    def test_init_db_path(self, mock_create_engine, mock_sessionmaker):
        db_path = "/db/path/database.db"
        DB(db_path=db_path)
        mock_create_engine.assert_called_with(
            f"sqlite+pysqlite:///{db_path}", echo=False
        )
        mock_sessionmaker.assert_called_with(bind=mock_create_engine.return_value)

    def test_metadata_creation(self):
        try:
            self.db.create_metadata()
        except Exception as e:
            self.fail(f"create_metadata raised exception {e}")
