import tkinter as tk

from services.habit_service import HabitService

from .views.create import CreateHabitView

# import views
from .views.habits import HabitsView


class Interface:
    """Main application interface."""

    def __init__(self, habit_service: HabitService):
        self._habit_service = habit_service
        self._root = tk.Tk()

        # basic tkinter settings
        self._root.title("indolent")
        self._root.geometry("500x600")

        self._open_main_window()

    def _open_main_window(self):
        """ "Open the main application window."""
        # create habit button
        _create_frame = tk.Frame(self._root)
        _create_frame.pack(fill="x")

        tk.Button(
            _create_frame, text="New Habit", command=self._open_create_window
        ).pack(pady=10)

        # habits list view
        self._habit_frame = tk.Frame(self._root)
        self._habit_frame.pack(fill="both", expand=True)

        self._view = HabitsView(self._habit_frame, self._habit_service)
        self._view.pack(fill="both", expand=True)
        self._view.refresh()

    def _open_create_window(self):
        """Open the create habit window."""
        view = CreateHabitView(
            self._root, self._habit_service, on_created=self._view.refresh
        )
        view.show()

    def run(self):
        """Run the main application loop."""
        self._root.mainloop()
