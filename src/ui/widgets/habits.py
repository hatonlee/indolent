"""Widgets for displaying habits."""

import tkinter as tk
from datetime import datetime, timedelta
from enum import Enum

from models.habit import Habit


class TimeUnit(Enum):
    SECOND = (1, "second", "seconds")
    MINUTE = (60, "minute", "minutes")
    HOUR = (3600, "hour", "hours")
    DAY = (86400, "day", "days")
    WEEK = (604800, "week", "weeks")

    @property
    def seconds(self) -> int:
        return self.value[0]

    @property
    def singular(self) -> str:
        return self.value[1]

    @property
    def plural(self) -> str:
        return self.value[2]


def format_timedelta(td: timedelta, n: int = 2) -> str:
    """Format a timedelta into the n highest non-zero units down to seconds."""
    total_seconds = int(td.total_seconds())

    counts = {}
    for unit in sorted(TimeUnit, key=lambda u: u.seconds, reverse=True):
        counts[unit] = total_seconds // unit.seconds
        total_seconds %= unit.seconds

    parts = []
    for unit, count in counts.items():
        if count <= 0:
            continue
        label = unit.singular if count == 1 else unit.plural
        parts.append(f"{count} {label}")

    return ", ".join(parts[:n]) if parts else "0 seconds"


class HabitFrame(tk.Frame):
    """A frame to display a habit."""

    def __init__(self, parent: tk.Widget, complete, habit: Habit, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self._complete = complete
        self._habit = habit
        self.config(padx=10, pady=10, borderwidth=3, relief="groove")
        self.columnconfigure(1, weight=1)
        self._render()

    def _render(self):
        """Create and layout the widgets for the habit frame."""
        self._render_details()
        self._render_status()

    def _render_details(self):
        self.details_frame = tk.Frame(self)
        self.details_frame.grid(row=0, column=0, sticky="nw")

        self._render_name()
        self._render_description()

    def _render_name(self):
        label_name = tk.Label(
            self.details_frame, text=self._habit.name, font=("Arial", 14, "bold")
        )
        label_name.grid(row=0, column=0, sticky="w")

    def _render_description(self):
        label_description = tk.Label(
            self.details_frame,
            text=str(self._habit.description),
            wraplength=200,
            justify="left",
        )
        label_description.grid(row=1, column=0, columnspan=3, sticky="w")

    def _render_status(self):
        now = datetime.now()
        completed = self._habit.completed(now)
        elapsed = now - self._habit.start_time
        frequency = self._habit.frequency
        current_interval_end = frequency - (elapsed % frequency)

        self.status_frame = tk.Frame(self)
        self.status_frame.grid(row=0, column=1, sticky="ne")
        self.status_frame.columnconfigure(0, weight=1)

        self._render_completed(completed)
        self._render_interval(completed, current_interval_end)
        self._render_frequency()

    def _render_completed(self, completed: bool):
        self.completed_frame = tk.Frame(self.status_frame)
        self.completed_frame.grid(row=0, column=1, sticky="e")

        self._render_completed_label(completed)
        self._render_complete_button(completed)

    def _render_completed_label(self, completed: bool):
        status_text = "Completed" if completed else "Not Completed"
        status_color = "green" if completed else "red"
        label_status = tk.Label(self.completed_frame, text=status_text, fg=status_color)
        label_status.grid(row=0, column=0, sticky="e")

    def _render_complete_button(self, completed: bool):
        button_complete = tk.Button(
            self.completed_frame, text="Complete", command=self._complete
        )
        if completed:
            button_complete.config(state="disabled")
        button_complete.grid(row=0, column=1, sticky="e", padx=(5, 0))

    def _render_interval(self, completed: bool, current_interval_end: timedelta):
        self.interval_frame = tk.Frame(self.status_frame)
        self.interval_frame.grid(row=1, column=0, columnspan=2, sticky="w")

        self._render_interval_label(completed)
        self._render_interval_time(current_interval_end)

    def _render_interval_label(self, completed):
        if completed:
            interval_text = "Next interval starts in:"
        else:
            interval_text = "Time remaining to complete:"

        label_interval = tk.Label(self.interval_frame, text=interval_text)
        label_interval.grid(row=1, column=0, sticky="w")

    def _render_interval_time(self, current_interval_end: timedelta):
        time_str = format_timedelta(current_interval_end)
        label_time = tk.Label(self.interval_frame, text=time_str)
        label_time.grid(row=1, column=1, sticky="w")

    def _render_frequency(self):
        self.frequency_frame = tk.Frame(self.status_frame)
        self.frequency_frame.grid(row=2, column=0, columnspan=2, sticky="w")

        self._render_frequency_label()
        self._render_frequency_time()

    def _render_frequency_label(self):
        label_frequency = tk.Label(self.frequency_frame, text="Frequency:")
        label_frequency.grid(row=2, column=0, sticky="w")

    def _render_frequency_time(self):
        time_str = format_timedelta(self._habit.frequency)
        label_time = tk.Label(self.frequency_frame, text=time_str)
        label_time.grid(row=2, column=1, sticky="w")


class HabitsList(tk.Frame):
    """A frame to display a list of habit frames."""

    def __init__(
        self,
        parent: tk.Widget,
        complete,
        habits: list[Habit] | None = None,
        *args,
        **kwargs,
    ):
        super().__init__(parent, *args, **kwargs)
        self._complete = complete
        self.habits = [] if habits is None else habits
        self.habit_frames = []
        self.config(padx=10, pady=10)
        self._render()

    def _render(self):
        self._clear()
        for habit in self.habits:
            self._render_habit_frame(habit)

    def _render_habit_frame(self, habit: Habit):
        habit_frame = HabitFrame(
            self,
            complete=lambda habit=habit: self._complete(habit.id),
            habit=habit,
        )
        self.habit_frames.append(habit_frame)
        habit_frame.pack(fill="x", pady=(0, 10))

    def _clear(self):
        for habit_frame in self.habit_frames:
            habit_frame.destroy()
        self.habit_frames = []


class HabitsCanvas(tk.Frame):
    """A scrollable canvas to display a habit list."""

    def __init__(self, parent, complete, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self._complete = complete
        canvas = tk.Canvas(self)
        self._habits_list = HabitsList(canvas, complete=self._complete)
        self._habits_list.bind(
            "<Configure>",
            lambda _: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        canvas.create_window((0, 0), window=self._habits_list, anchor="nw")

        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill=tk.Y)
        self._habits_list.pack(fill="both", expand=True)

    def render(self, habits: list[Habit]):
        self._habits_list.habits = habits
        self._habits_list._render()


class DailyHabits:
    pass
