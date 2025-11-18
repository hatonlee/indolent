from entities.habit_entity import Habit
from sqlalchemy.orm import Session

class HabitRepository:

    def __init__(self, db: Session):
        self.db = db

    def add(self, habit: Habit):
        self.db.add(habit)
        self.db.commit()
        return habit

    def list(self):
        return self.db.query(Habit).all()

    def get_by_name(self, name: str):
        return self.db.query(Habit).filter(Habit.name == name).first()