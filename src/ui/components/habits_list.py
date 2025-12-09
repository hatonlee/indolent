"""UI Component: Habits List"""

import tkinter as tk


class HabitsList(tk.Frame):
    """UI Component: renders a list of habits into a container frame."""

    def __init__(self, parent, mark_done_callback):
        super().__init__(parent)
        self._mark_done = mark_done_callback

    def render(self, habits):
        for widget in self.winfo_children():
            widget.destroy()

        for habit in habits:
            self._create_habit_card(habit)

    def _create_habit_card(self, habit):
        frame = tk.Frame(self, bd=2, relief="solid", padx=10, pady=10)
        frame.pack(fill="x", pady=5)

        tk.Label(frame, text=habit.name, font=("Arial", 12, "bold")).pack(anchor="w")
        tk.Label(frame, text=habit.description).pack(anchor="w")
        tk.Label(frame, text=f"Frequency: {habit.frequency}").pack(anchor="w")
        tk.Label(frame, text=f"Last Done: {habit.last_done}").pack(anchor="w")

        if not getattr(habit, "done", False):
            tk.Button(
                frame,
                text="Mark Done",
                command=lambda hid=habit.id: self._mark_done(hid),
            ).pack(anchor="e", pady=5)
