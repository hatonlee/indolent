"""Repository layer class for habit."""

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from db import session as default_session
from models.habit import Habit


class HabitRepository:
    """Provide methods for getting and creating habits."""

    def __init__(self, session: sessionmaker = default_session):
        self._session = session

    def get_all(self):
        """Get all habits."""
        with self._session() as session:
            habits = session.scalars(select(Habit))
            return list(habits)

    def get_undone(self):
        """Get all habits whose last_done is not the current iteration"""
        with self._session() as session:
            habits = list(session.scalars(select(Habit)))
            for habit in habits:
                if datetime.now() - habit.last_done < habit.frequency:
                    habits.pop(habit)
            return habits

    def get(self, habit_id: int = None):
        """Get habit with a specific id. The first habit is returned if id is not specified"""
        with self._session() as session:
            if habit_id is None:
                habit = session.scalar(select(Habit))
            else:
                habit = session.scalar(select(Habit).where(Habit.id == habit_id))
            return habit

    def get_by_name(self, name: str):
        """Get habit with a specific name"""
        with self._session() as session:
            habit = session.scalar(select(Habit).where(Habit.name == name))
            return habit

    def add(self, habit_data: dict):
        """Add a new habit to the database"""
        with self._session.begin() as session:
            habit = Habit(**habit_data)
            session.add(habit)
            return habit

    def mark_done(self, habit_id: int):
        with self._session.begin() as session:
            habit = session.scalar(select(Habit).where(Habit.id == habit_id))
            if not habit:
                raise ValueError(f"Habit with id '{habit_id}' not found")
            habit.last_done = datetime.now()
            return habit


default_habit_repository = HabitRepository()
