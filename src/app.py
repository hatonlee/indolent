from db import Base, engine, SessionLocal
from repositories.habit_repository import HabitRepository
from services.habit_service import HabitService
from ui.ui import Interface
import tkinter as tk

def main():
    # initialize database
    Base.metadata.create_all(bind=engine)

    # initialize dependencies
    db = SessionLocal()
    repo = HabitRepository(db)
    service = HabitService(repo)

    # tkinter ui
    root = tk.Tk()
    app = Interface(root, service)
    root.mainloop()

if __name__ == "__main__":
    main()