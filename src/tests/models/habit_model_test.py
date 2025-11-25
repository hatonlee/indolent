import unittest

from models.habit import Habit


class TestHabit(unittest.TestCase):
    def setUp(self):
        self.habit = Habit(name="name", description="description")

    def test_habit_creation_succeeds(self):
        self.assertEqual(
            repr(self.habit), f"Habit(id={self.habit.id}, name='{self.habit.name}')"
        )
