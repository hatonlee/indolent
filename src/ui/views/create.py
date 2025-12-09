import tkinter as tk

from ..components.new_habit_form import NewHabitForm


class CreateHabitView:
    """View: opens a Toplevel with the `NewHabitForm` component."""

    def __init__(self, parent, habit_service, on_created=None):
        self._parent = parent
        self._service = habit_service
        self._on_created = on_created

    def show(self):
        """Opens the Toplevel window with the form."""
        win = tk.Toplevel(self._parent)
        win.title("New Habit")
        win.geometry("300x250")

        def _on_create(data):
            self._service.add(data)
            win.destroy()
            if callable(self._on_created):
                self._on_created()

        form = NewHabitForm(win, on_create=_on_create)
        form.pack(fill="both", expand=True, padx=10, pady=10)
