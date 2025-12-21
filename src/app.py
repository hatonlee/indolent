"""Run the app"""

from pathlib import Path

from db import DB
from repositories.habit_repository import HabitRepository
from services.habit_service import HabitService
from ui.ui import UI


def main():
    # initialize database
    DB_PATH = Path(__file__).parent.parent / "database.db"
    db = DB(DB_PATH.as_posix())
    db.create_metadata()

    # initialize service
    repo = HabitRepository(db)
    service = HabitService(repo)

    # initialize and run the app
    app = UI(service)
    app.run()


if __name__ == "__main__":
    main()
