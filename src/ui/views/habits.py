import tkinter as tk

from ..components.habits_list import HabitsList


class HabitsView(tk.Frame):
    """View: displays habits using a scrollable area and the `HabitsList` component."""

    def __init__(self, parent, habit_service):
        super().__init__(parent)
        self._service = habit_service

        self._canvas = tk.Canvas(self)
        self._container = tk.Frame(self._canvas)
        self._container.bind(
            "<Configure>",
            lambda _: self._canvas.configure(scrollregion=self._canvas.bbox("all")),
        )
        self._canvas.create_window((0, 0), window=self._container, anchor="nw")

        scrollbar = tk.Scrollbar(self, orient="vertical", command=self._canvas.yview)
        self._canvas.configure(yscrollcommand=scrollbar.set)

        self._canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        habits = HabitsList(self._container, mark_done_callback=self._mark_done)
        habits.pack(fill="both", expand=True)

    def refresh(self):
        """Fetch habits and refresh the list."""
        habits = self._service.get_all()
        not_done = [h for h in habits if not h.done]
        done = [h for h in habits if h.done]

        for widget in self._container.winfo_children():
            widget.destroy()

        tk.Label(self._container, text="Not Done", font=("Helvetica", 14, "bold")).pack(
            anchor="w", pady=10
        )
        habits_done = HabitsList(self._container, mark_done_callback=self._mark_done)
        habits_done.pack(fill="both", expand=True)
        habits_done.render(not_done)

        tk.Label(self._container, text="Done", font=("Helvetica", 14, "bold")).pack(
            anchor="w", pady=10
        )
        habits_not_done = HabitsList(
            self._container, mark_done_callback=self._mark_done
        )
        habits_not_done.pack(fill="both", expand=True)
        habits_not_done.render(done)

    def _mark_done(self, habit_id):
        self._service.mark_done(habit_id)
        self.refresh()
