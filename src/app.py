"""Run the app"""

from pathlib import Path

from db import DB
from repositories.habit_repository import HabitRepository
from services.habit_service import HabitService
from ui.ui import UI

DB_PATH = Path(__file__).parent.parent / "database.db"


def main(db_path: Path) -> None:
    """Initialize and run the app"""
    # initialize database
    db = DB(db_path.as_posix())
    db.create_metadata()

    # initialize service
    repo = HabitRepository(db)
    service = HabitService(repo)

    # initialize and run the app
    app = UI(service)
    app.run()


if __name__ == "__main__":
    main(DB_PATH)
