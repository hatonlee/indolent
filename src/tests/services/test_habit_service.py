import unittest
from datetime import datetime

from repositories.habit_repository import HabitRepository
from services.habit_service import HabitService
from tests.base import BaseTestCase


class TestHabitService(BaseTestCase):
    def setUp(self):
        super().setUp()
        repo = HabitRepository(session=self.session)
        self.service = HabitService(repo=repo)

        self.data = {
            "name": "name",
            "description": "description",
            "start_time": datetime.now(),
            "frequency": 60,
        }

    def test_get_returns_habit(self):
        self.service.add(self.data)
        habit = self.service.get()
        self.assertIsNotNone(habit)
        self.assertEqual(habit.name, "name")

    def test_add_duplicate_fails(self):
        self.service.add(self.data)

        with self.assertRaises(ValueError):
            self.service.add(self.data)
