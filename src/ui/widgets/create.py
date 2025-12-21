"""Widgets for creating new habits."""

import tkinter as tk
from datetime import datetime, timedelta
from tkinter import messagebox
from tkinter import ttk as ttk


class CreateHabitFrame(tk.Frame):
    """A frame to create a new habit."""

    def __init__(self, parent: tk.Widget | tk.Toplevel, on_create):
        super().__init__(parent)
        self.on_create = on_create
        self.columnconfigure(1, weight=1)
        self._create_widgets()

    def _create_widgets(self):
        """Create and layout the widgets for the new habit form."""
        title_label = tk.Label(self, text="Create New Habit", font=("Arial", 16))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        name_label = tk.Label(self, text="Name:")
        name_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self._name_entry = tk.Entry(self)
        self._name_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        desc_label = tk.Label(self, text="Description:")
        desc_label.grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self._desc_entry = tk.Entry(self)
        self._desc_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        start_time_label = tk.Label(self, text="Start Time:")
        start_time_label.grid(row=3, column=0, sticky="e", padx=5, pady=5)

        now = datetime.now()
        self._start_time_year_combobox = ttk.Combobox(
            self, values=[str(y) for y in range(now.year - 1, now.year + 10)], width=5
        )
        self._start_time_year_combobox.grid(row=3, column=1, sticky="w", padx=5, pady=5)
        self._start_time_year_combobox.set(str(now.year))

        self._start_time_month_combobox = ttk.Combobox(
            self, values=[str(m) for m in range(1, 12 + 1)], width=3
        )
        self._start_time_month_combobox.grid(row=3, column=1, padx=60, pady=5)
        self._start_time_month_combobox.set(str(now.month))

        self._start_time_day_combobox = ttk.Combobox(
            self, values=[str(d) for d in range(1, 31 + 1)], width=3
        )
        self._start_time_day_combobox.grid(row=3, column=1, sticky="e", padx=5, pady=5)
        self._start_time_day_combobox.set(str(now.day))

        self._start_time_hour_combobox = ttk.Combobox(
            self, values=[str(h) for h in range(0, 23 + 1)], width=3
        )
        self._start_time_hour_combobox.grid(row=4, column=1, sticky="w", padx=5, pady=5)
        self._start_time_hour_combobox.set(str(now.hour))

        self._start_time_minute_combobox = ttk.Combobox(
            self, values=[str(m) for m in range(0, 59 + 1)], width=3
        )
        self._start_time_minute_combobox.grid(
            row=4, column=1, sticky="e", padx=5, pady=5
        )
        self._start_time_minute_combobox.set(str(now.minute))

        freq_label = tk.Label(self, text="Frequency (minutes):")
        freq_label.grid(row=5, column=0, sticky="e", padx=5, pady=5)
        self._freq_entry = tk.Entry(self)
        self._freq_entry.grid(row=5, column=1, sticky="ew", padx=5, pady=5)

        submit_button = tk.Button(self, text="Create", command=self._create)
        submit_button.grid(row=6, column=0, columnspan=2, pady=10)

    def _create(self):
        name = self._name_entry.get().strip()
        desc = self._desc_entry.get().strip()
        year = self._start_time_year_combobox.get().strip()
        month = self._start_time_month_combobox.get().strip()
        day = self._start_time_day_combobox.get().strip()
        hour = self._start_time_hour_combobox.get().strip()
        minute = self._start_time_minute_combobox.get().strip()
        freq = self._freq_entry.get().strip()

        if not self._validate_name(name):
            messagebox.showerror(
                "Invalid Input", "Name must be between 1 and 100 characters."
            )
            return

        if not self._validate_description(desc):
            messagebox.showerror(
                "Invalid Input", "Description must be 255 characters or fewer."
            )
            return

        if not self._validate_datetime(year, month, day, hour, minute):
            messagebox.showerror(
                "Invalid Input", "Start time is not a valid date/time."
            )
            return

        if not self._validate_frequency(freq):
            messagebox.showerror(
                "Invalid Input", "Frequency must be a positive integer."
            )
            return

        start_time = datetime(int(year), int(month), int(day), int(hour), int(minute))
        freq = timedelta(minutes=int(freq))

        data = {
            "name": name,
            "description": desc,
            "start_time": start_time,
            "frequency": freq,
        }

        if callable(self.on_create):
            self.on_create(data)

    def _validate_name(self, name):
        """Validate the habit name."""
        return 100 > len(name) > 0

    def _validate_description(self, description):
        """Validate the habit description."""
        return 255 >= len(description) >= 0

    def _validate_datetime(self, year, month, day, hour, minute):
        """Validate the provided date and time components."""
        try:
            datetime(int(year), int(month), int(day), int(hour), int(minute))
            return True
        except ValueError:
            return False

    def _validate_frequency(self, frequency):
        """Validate the frequency"""
        try:
            freq = int(frequency)
            return freq > 0
        except ValueError:
            return False


class CreateHabitWindow:
    def __init__(self, parent: tk.Tk, on_create):
        self._parent = parent
        self._on_create = on_create
        self._show_window()

    def _show_window(self):
        """Open the window."""
        win = tk.Toplevel(self._parent)
        win.title("Create a new Habit")
        win.geometry("300x250")

        def _on_create(data):
            win.destroy()
            if callable(self._on_create):
                self._on_create(data)

        form = CreateHabitFrame(win, on_create=_on_create)
        form.pack(fill="both", expand=True, padx=10, pady=10)
