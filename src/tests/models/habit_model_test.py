import unittest
from datetime import datetime

from models.habit import Habit


class TestHabit(unittest.TestCase):
    def setUp(self):
        self.habit = Habit(
            name="name",
            description="description",
            start_time=datetime.now(),
            frequency=60,
        )

    def test_habit_attributes(self):
        self.assertEqual(self.habit.name, "name")
        self.assertEqual(self.habit.description, "description")
        self.assertEqual(self.habit.frequency, 60)

    def test_habit_repr(self):
        r = repr(self.habit)
        self.assertEqual(
            r,
            f"Habit(\
            name={self.habit.name}, description={self.habit.description},\
            frequency{self.habit.frequency}, start_time={self.habit.start_time},\
            frequency={self.habit.frequency}, last_done={self.habit.last_done}\
        )",
        )
