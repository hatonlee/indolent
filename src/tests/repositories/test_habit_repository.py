from datetime import datetime, timedelta

from repositories.habit_repository import HabitRepository
from tests.base import BaseTestCase


class TestHabitRepository(BaseTestCase):
    def setUp(self):
        super().setUp()

        self.repo = HabitRepository(self.db)

        self.data = {
            "name": "test_name",
            "description": "test_description",
            "start_time": datetime.now(),
            "frequency": timedelta(days=1),
        }

    def test_add(self):
        habit = self.repo.add(self.data)
        self.assertIsNotNone(habit)
        self.assertIsNotNone(habit.id)

    def test_get(self):
        self.repo.add(self.data)
        habit = self.repo.get()
        self.assertIsNotNone(habit)
        if habit:
            self.assertEqual(habit.name, "test_name")

    def test_find(self):
        self.repo.add(self.data)
        habits = self.repo.find()
        self.assertIsInstance(habits, list)

    def test_find_with_filters(self):
        self.repo.add(self.data)
        habits = self.repo.find(name="test_name")
        self.assertIsInstance(habits, list)
        self.assertGreaterEqual(len(habits), 1)

    def test_find_with_invalid_filter(self):
        self.repo.add(self.data)
        with self.assertRaises(ValueError):
            self.repo.find(invalid_filter="value")

    def test_find_with_none(self):
        self.repo.add(self.data)
        habits = self.repo.find(name=None)
        self.assertIsInstance(habits, list)
        self.assertGreaterEqual(len(habits), 1)

    def test_complete(self):
        habit = self.repo.add(self.data)
        completed = self.repo.complete(habit.id, datetime.now())
        self.assertIsNotNone(completed)
        self.assertEqual(len(completed.completions), 1)

    def test_complete_nonexistent_habit(self):
        with self.assertRaises(ValueError):
            self.repo.complete(-1, datetime.now())

    def test_complete_different_interval(self):
        habit = self.repo.add(self.data)
        self.repo.complete(habit.id, datetime.now())
        self.repo.complete(habit.id, datetime.now() + timedelta(days=1))
        completed = self.repo.get(habit.id)
        self.assertIsNotNone(completed)
        if completed:
            self.assertEqual(len(completed.completions), 2)

    def test_complete_same_interval(self):
        habit = self.repo.add(self.data)
        self.repo.complete(habit.id, datetime.now())
        self.repo.complete(habit.id, datetime.now())
        completed = self.repo.get(habit.id)
        self.assertIsNotNone(completed)
        if completed:
            self.assertEqual(len(completed.completions), 1)

    def test_delete_all(self):
        self.repo.add(self.data)
        self.repo.delete_all()
        habits = self.repo.find()
        self.assertIsInstance(habits, list)
        self.assertEqual(len(habits), 0)
