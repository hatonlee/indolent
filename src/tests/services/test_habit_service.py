from datetime import datetime, timedelta

from repositories.habit_repository import HabitRepository
from services.habit_service import HabitService
from tests.base import BaseTestCase


class TestHabitService(BaseTestCase):
    def setUp(self):
        super().setUp()
        repo = HabitRepository(self.db)
        self.service = HabitService(repo)

        self.data = {
            "name": "test_name",
            "description": "test_description",
            "start_time": datetime.now(),
            "frequency": timedelta(days=1),
        }

    def test_add(self):
        habit = self.service.add(self.data)
        self.assertIsNotNone(habit)
        self.assertIsNotNone(habit.id)

    def test_add_duplicate_name_raises(self):
        self.service.add(self.data)
        with self.assertRaises(ValueError):
            self.service.add(self.data)

    def test_get(self):
        habit_added = self.service.add(self.data)
        habit = self.service.get(habit_added.id)
        self.assertIsNotNone(habit)
        if habit:
            self.assertEqual(habit.name, "test_name")

    def test_find(self):
        self.service.add(self.data)
        habits = self.service.find(name="test_name")
        self.assertIsInstance(habits, list)
        self.assertEqual(len(habits), 1)
        self.assertEqual(habits[0].name, "test_name")

    def test_complete(self):
        habit = self.service.add(self.data)
        completed_habit = self.service.complete(habit.id, datetime.now())
        self.assertIsNotNone(completed_habit)
        self.assertEqual(len(completed_habit.completions), 1)
