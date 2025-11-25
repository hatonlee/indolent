"""Service layer class for habit."""

from repositories.habit_repository import HabitRepository, default_habit_repository


class HabitService:
    """Provide methods for getting and creating habits."""

    def __init__(self, repo: HabitRepository = default_habit_repository):
        self._repo = repo

    def get_all(self):
        return self._repo.get_all()

    def add(self, habit_data):
        if self._repo.get_by_name(habit_data["name"]):
            raise ValueError("Habit already exists.")

        return self._repo.add(habit_data)


default_habit_service = HabitService()
