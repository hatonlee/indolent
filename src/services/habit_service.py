"""Service layer class for habit."""

from datetime import datetime

from models.habit import Habit
from repositories.habit_repository import HabitRepository


class HabitService:
    """Service for managing habits."""

    def __init__(self, repo: HabitRepository):
        self._repo = repo

    def get(self, habit_id: int) -> Habit | None:
        return self._repo.get(habit_id)

    def find(self, **filters: str) -> list[Habit]:
        return self._repo.find(**filters)

    def add(self, habit_data: dict[str, str | list]) -> Habit:
        """Add a new habit"""
        if self._repo.find(name=str(habit_data.get("name"))):
            raise ValueError("Habit with the same name already exists.")

        return self._repo.add(habit_data)

    def complete(self, habit_id: int, time: datetime) -> Habit:
        return self._repo.complete(habit_id, time)
