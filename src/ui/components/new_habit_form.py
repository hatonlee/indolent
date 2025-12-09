import tkinter as tk
from datetime import datetime
from tkinter import messagebox


class NewHabitForm(tk.Frame):
    """UI Component: new habit form."""

    def __init__(self, parent, on_create):
        super().__init__(parent)
        self.on_create = on_create

        tk.Label(self, text="Name").pack()
        self._name_entry = tk.Entry(self)
        self._name_entry.pack()

        tk.Label(self, text="Description").pack()
        self._desc_entry = tk.Entry(self)
        self._desc_entry.pack()

        tk.Label(self, text="Frequency (minutes)").pack()
        self._freq_entry = tk.Entry(self)
        self._freq_entry.pack()

        tk.Button(self, text="Create", command=self._create).pack(pady=10)

    def _create(self):
        name = self._name_entry.get().strip()
        desc = self._desc_entry.get().strip()
        freq_text = self._freq_entry.get().strip()

        if not name:
            messagebox.showerror("Error", "Name required")
            return

        if not freq_text:
            messagebox.showerror("Error", "Frequency required")
            return

        try:
            freq = int(freq_text)
        except ValueError:
            messagebox.showerror("Error", "Frequency must be an integer")
            return

        data = {
            "name": name,
            "description": desc,
            "start_time": datetime.now(),
            "frequency": freq,
            "last_done": None,
        }

        if callable(self.on_create):
            self.on_create(data)
