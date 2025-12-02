"""Run the app"""

from db import Base, engine, session
from repositories.habit_repository import HabitRepository
from services.habit_service import HabitService
from ui.ui import Interface


def main():
    # initialize database
    Base.metadata.create_all(bind=engine)

    # initialize dependencies
    repo = HabitRepository(session)
    service = HabitService(repo)

    # tkinter ui
    app = Interface(service)
    app.run()


if __name__ == "__main__":
    main()
