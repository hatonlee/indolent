from datetime import datetime

from repositories.habit_repository import HabitRepository
from tests.base import BaseTestCase


class TestHabitRepository(BaseTestCase):
    def setUp(self):
        super().setUp()

        self.repo = HabitRepository(session=self.session)

        self.data = {
            "name": "name",
            "description": "description",
            "start_time": datetime.now(),
            "frequency": 60,
        }

    def test_add(self):
        habit = self.repo.add(self.data)
        self.assertIsNotNone(habit)
        self.assertIsNotNone(habit.id)

    def test_get(self):
        self.repo.add(self.data)
        habit = self.repo.get()
        self.assertIsNotNone(habit)
        self.assertEqual(habit.name, "name")

    def test_get_all(self):
        self.repo.add(self.data)
        habits = self.repo.get_all()
        self.assertIsInstance(habits, list)

    def test_get_all_has_done_attribute(self):
        self.repo.add(self.data)
        habits = self.repo.get_all()
        self.assertTrue(hasattr(habits[0], "done"))

    def test_mark_done_sets_last_done(self):
        habit = self.repo.add(self.data)
        self.repo.mark_done(habit.id)
        self.assertIsNotNone(habit.last_done)
