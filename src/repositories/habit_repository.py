"""API for performing CRUD operations on habits in the database."""

from datetime import datetime

from sqlalchemy import delete, select
from sqlalchemy.orm import joinedload

from db import DB
from models.habit import Completion, Habit


class HabitRepository:
    """API for performing CRUD operations on habits in the database."""

    def __init__(self, db: DB):
        self._db = db

    def _build_query(self, **filters: str):
        stmt = select(Habit)
        for key, value in filters.items():
            if not hasattr(Habit, key):
                raise ValueError(f"Invalid filter: '{key}'")
            if value is None:
                continue
            attr = getattr(Habit, key)
            stmt = stmt.where(attr == value)

        return stmt

    def get(self, habit_id: int | None = None) -> Habit | None:
        with self._db.session() as session:
            stmt = select(Habit).options(joinedload(Habit.completions))
            if habit_id is None:
                habit = session.scalar(stmt)
            else:
                stmt = stmt.where(Habit.id == habit_id)
                habit = session.scalar(stmt)

        return habit

    def find(self, **filters: str) -> list[Habit]:
        with self._db.session() as session:
            stmt = self._build_query(**filters)
            stmt = stmt.options(joinedload(Habit.completions))
            habits = list(session.scalars(stmt).unique())

        return habits

    def add(self, habit_data: dict) -> Habit:
        """Add a new habit to the database"""
        with self._db.begin() as session:
            habit = Habit(**habit_data)
            session.add(habit)
            session.flush()

            # load completions
            _ = habit.completions

        return habit

    def complete(self, habit_id: int, time: datetime) -> Habit:
        """Add a completion entry for the habit if one does not already exist for the specified interval."""
        with self._db.begin() as session:
            habit = session.scalar(select(Habit).where(Habit.id == habit_id))
            if not habit:
                raise ValueError(f"Habit with id '{habit_id}' not found")
            if not habit.completed(time):
                habit.completions.append(Completion(time=time))

        return habit

    def delete_all(self) -> None:
        """Delete all habits from the database."""
        with self._db.begin() as session:
            session.execute(delete(Habit))
