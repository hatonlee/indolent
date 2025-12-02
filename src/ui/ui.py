import tkinter as tk
from datetime import datetime, timedelta
from tkinter import messagebox, ttk

from services.habit_service import HabitService


class Interface:
    def __init__(self, habit_service: HabitService):
        self._habit_service = habit_service
        self._root = tk.Tk()

        # basic tkinter settings
        self._root.title("indolent")
        self._root.geometry("350x300")

        self._init_ui()

    def _init_ui(self):
        # new habit button
        top_frame = tk.Frame(self._root)
        top_frame.pack(fill="x")

        tk.Button(top_frame, text="New Habit", command=self._open_create_window).pack(
            pady=10
        )

        # container for habits
        self.canvas = tk.Canvas(self._root)
        scrollbar = tk.Scrollbar(
            self._root, orient="vertical", command=self.canvas.yview
        )
        self._container = tk.Frame(self.canvas)

        self._container.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        self.canvas.create_window((0, 0), window=self._container, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self._reload_habits()

    def _reload_habits(self):
        # remove existing reference cards
        for widget in self._container.winfo_children():
            widget.destroy()

        # divide habits between done and not done
        habits = self._habit_service.get_all()
        for habit in habits:
            if habit.last_done:
                time_diff = datetime.now() - habit.last_done
                frequency = timedelta(minutes=int(habit.frequency))
                habit.done = time_diff < frequency
            else:
                habit.done = False
        done = [h for h in habits if h.done]
        not_done = [h for h in habits if not h.done]

        # add habits that are not done
        tk.Label(self._container, text="Not Done", font=("Arial", 14, "bold")).pack(
            anchor="w", pady=10
        )
        for habit in not_done:
            self._create_habit_card(habit)

        # add habits that are done
        tk.Label(self._container, text="Done", font=("Arial", 14, "bold")).pack(
            anchor="w", pady=10
        )
        for habit in done:
            self._create_habit_card(habit)

    def _create_habit_card(self, habit):
        # create frame
        frame = tk.Frame(self._container, bd=2, relief="solid", padx=10, pady=10)
        frame.pack(fill="x", pady=5)

        # add info
        tk.Label(frame, text=habit.name, font=("Arial", 12, "bold")).pack(anchor="w")
        tk.Label(frame, text=habit.description).pack(anchor="w")
        tk.Label(frame, text=f"Frequency: {habit.frequency}").pack(anchor="w")
        tk.Label(frame, text=f"Last Done: {habit.last_done}").pack(anchor="w")

        if not habit.done:
            tk.Button(
                frame, text="Mark Done", command=lambda h=habit: self._mark_done(h.id)
            ).pack(anchor="e", pady=5)

    def _mark_done(self, habit_id):
        self._habit_service.mark_done(habit_id)
        self._reload_habits()

    def _open_create_window(self):
        win = tk.Toplevel(self._root)
        win.title("New Habit")
        win.geometry("300x250")

        tk.Label(win, text="Name").pack()
        name_entry = tk.Entry(win)
        name_entry.pack()

        tk.Label(win, text="Description").pack()
        desc_entry = tk.Entry(win)
        desc_entry.pack()

        tk.Label(win, text="Frequency (minutes)").pack()
        freq_entry = tk.Entry(win)
        freq_entry.pack()

        def create():
            name = name_entry.get().strip()
            desc = desc_entry.get().strip()
            freq = int(freq_entry.get().strip())

            if not name:
                messagebox.showerror("Error", "Name required")
                return

            if not freq:
                messagebox.showerror("Error", "Frequency required")
                return

            self._habit_service.add(
                {
                    "name": name,
                    "description": desc,
                    "start_time": datetime.now(),
                    "frequency": freq,
                    "last_done": None,
                }
            )

            win.destroy()
            self._reload_habits()

        tk.Button(win, text="Create", command=create).pack(pady=10)

    def run(self):
        self._root.mainloop()
