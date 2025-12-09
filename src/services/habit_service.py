"""Service layer class for habit."""

from repositories.habit_repository import HabitRepository, default_habit_repository


class HabitService:
    """Provide methods for getting and creating habits."""

    def __init__(self, repo: HabitRepository = default_habit_repository):
        self._repo = repo

    def get_all(self):
        """Get all habits with their done status."""
        return self._repo.get_all()

    def add(self, habit_data):
        """Add a new habit"""
        if self._repo.get_by_name(habit_data["name"]):
            raise ValueError("Habit with the same name already exists.")

        return self._repo.add(habit_data)

    def mark_done(self, habit_id: int):
        """Mark a habit as done."""
        return self._repo.mark_done(habit_id)


default_habit_service = HabitService()
