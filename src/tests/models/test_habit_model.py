import unittest
from datetime import datetime, timedelta

from models.habit import Completion, Habit


class TestHabit(unittest.TestCase):
    def setUp(self):
        self.habit = Habit(
            id=1,
            name="test_name",
            description="test_description",
            start_time=datetime(2024, 1, 1, 0, 0, 0),
            frequency=timedelta(days=1),
            completions=[],
        )

    def test_completed_no_completions(self):
        self.assertFalse(self.habit.completed())

    def test_completed_within_datetime(self):
        completion_time = datetime(2024, 1, 2, 12, 0, 0)
        self.habit.completions.append(
            Completion(id=1, time=completion_time, habit_id=self.habit.id)
        )
        self.assertTrue(self.habit.completed(datetime(2024, 1, 2, 15, 0, 0)))

    def test_completed_outside_datetime(self):
        completion_time = datetime(2024, 1, 2, 12, 0, 0)
        self.habit.completions.append(
            Completion(id=1, time=completion_time, habit_id=self.habit.id)
        )
        self.assertFalse(self.habit.completed(datetime(2024, 1, 3, 1, 0, 0)))

    def test_completed_within_interval(self):
        completion_time = datetime(2024, 1, 2, 12, 0, 0)
        self.habit.completions.append(
            Completion(id=1, time=completion_time, habit_id=self.habit.id)
        )
        self.assertTrue(self.habit.completed(1))

    def test_completed_outside_interval(self):
        completion_time = datetime(2024, 1, 2, 12, 0, 0)
        self.habit.completions.append(
            Completion(id=1, time=completion_time, habit_id=self.habit.id)
        )
        self.assertFalse(self.habit.completed(2))

    def test_habit_repr(self):
        expected_repr = "<Habit(id=1, name='test_name', start_time=datetime.datetime(2024, 1, 1, 0, 0)), frequency=1 day, 0:00:00, done=False)>"
        self.assertEqual(repr(self.habit), expected_repr)

    def test_completion_repr(self):
        completion = Completion(
            id=1,
            time=datetime(2024, 1, 2, 12, 0, 0),
            habit_id=self.habit.id,
            habit=self.habit,
        )
        expected_repr = (
            "<Completion(id=1, time=datetime.datetime(2024, 1, 2, 12, 0), habit_id=1)>"
        )
        self.assertEqual(repr(completion), expected_repr)
