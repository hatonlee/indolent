"""Repository layer class for habit."""

from sqlalchemy import select
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import sessionmaker

from db import session as default_session
from models.habit import Habit


class HabitRepository:
    """Provide methods for getting and creating habits."""

    def __init__(self, session: sessionmaker = default_session):
        self._session = session

    def _to_dict(self, obj):
        """Returns a dictionary representation of the object"""
        return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}

    def get_all(self):
        """Get data of one unspecified habit"""
        with self._session() as session:
            habits = session.scalars(select(Habit))
            return [self._to_dict(habit) for habit in habits]

    def get(self):
        """Get data of all habits"""
        with self._session() as session:
            habit = session.scalar(select(Habit))
            return self._to_dict(habit) if habit else None

    def get_by_name(self, name: str):
        """Get data of one habit with a certain name"""
        with self._session() as session:
            habit = session.scalar(select(Habit).where(Habit.name == name))
            return self._to_dict(habit) if habit else None

    def add(self, habit_data: dict):
        """Add a new habit to the database"""
        with self._session() as session:
            habit = Habit(**habit_data)
            session.add(habit)
            session.commit()
            return self._to_dict(habit)


default_habit_repository = HabitRepository()
