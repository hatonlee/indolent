import tkinter as tk
from datetime import datetime

from services.habit_service import HabitService

from .widgets.actionbar import ActionBar
from .widgets.create import CreateHabitWindow
from .widgets.habits import HabitFrame, HabitsFrame


class WindowManager:
    """Register and manage layouts."""

    def __init__(self):
        self.layouts = {}
        self.current = None

    def register(self, name: str, layout: Layout):
        """Register a layout."""
        self.layouts[name] = layout

    def switch(self, name: str):
        layout = self.layouts.get(name)
        if not layout:
            raise ValueError(f"Layout '{name}' not found.")

        if self.current:
            self.current.destroy()
            self.current = None

        layout.render()
        self.current = layout


class Layout:
    """Base class for layouts."""

    def __init__(self, root: tk.Tk):
        self.root = root

    def render(self):
        """Render the layout."""
        raise NotImplementedError

    def destroy(self):
        """Destroy the layout."""
        self.root.destroy()


class MainLayout(Layout):
    """Main application layout containing habit list and actions."""

    def __init__(self, root: tk.Tk, habit_service: HabitService):
        super().__init__(root)
        self._service = habit_service
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

    def render(self):
        self._render_actions_frame()
        self._render_habits_frame()
        self._refresh_habits()

    def _render_actions_frame(self):
        actions_frame = ActionBar(self.root, self._open_create_window)
        actions_frame.grid(row=0, column=0, sticky="ew")
        actions_frame.columnconfigure(0, weight=1)

    def _render_habits_frame(self):
        self.habits_frame = HabitsFrame(self.root, complete_cb=self._complete)
        self.habits_frame.configure(padx=5, pady=5, bg="blue")
        self.habits_frame.grid(row=1, column=0, sticky="nsew")
        self.habits_frame.columnconfigure(0, weight=1)
        self.habits_frame.rowconfigure(0, weight=1)

    def _refresh_habits(self):
        self.habits_frame.render(self._service.find())

    def _complete(self, habit_id: int, habit_frame: HabitFrame):
        habit = self._service.complete(habit_id, datetime.now())
        habit_frame.habit = habit
        habit_frame.refresh_status()

    def _add_habit(self, habit_data: dict[str, str | list]):
        new_habit = self._service.add(habit_data)
        self.habits_frame.append_habit(new_habit)

    def _open_create_window(self):
        CreateHabitWindow(self.root, self._add_habit)


class UI:
    """Main UI class to initialize and run the application."""

    def __init__(self, habit_service: HabitService):
        self._habit_service = habit_service
        self._root = tk.Tk()

        self._root.title("indolent")
        self._root.geometry("500x600")

        self._manager = WindowManager()
        self._manager.register("main", MainLayout(self._root, self._habit_service))

    def run(self):
        """Open the main layout and start the main loop."""
        self._manager.switch("main")
        self._root.mainloop()
