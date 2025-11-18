from entities.habit_entity import Habit
from repositories.habit_repository import HabitRepository

class HabitService:

    def __init__(self, repository: HabitRepository):
        self.repository = repository

    def add(self, name: str, description: str):
        if self.repository.get_by_name(name):
            raise ValueError("Habit already exists.")

        habit = Habit(name=name, description=description)
        return self.repository.add(habit)

    def list(self):
        return self.repository.list()