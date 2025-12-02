import unittest

from models.habit import Habit


class TestHabit(unittest.TestCase):
    def setUp(self):
        self.habit = Habit(name="name", description="description")

    def test_habit_exists(self):
        self.assertIsNotNone(self.habit)

    def test_habit_repr(self):
        self.assertEqual(
            repr(self.habit),
            f"Habit(id={self.habit.id}, name='{self.habit.name}', description='{self.habit.description}')",
        )
