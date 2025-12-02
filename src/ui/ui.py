import tkinter as tk
from tkinter import messagebox

from services.habit_service import HabitService


class Interface:
    def __init__(self, habit_service: HabitService):
        self._habit_service = habit_service
        self._root = tk.Tk()

        # define widgets
        self._habit_list = None
        self._name_input = None
        self._desc_input = None

        # load widgets
        self._init_ui()

    def _init_ui(self):
        # basic tkinter settings
        self._root.title("indolent")
        self._root.geometry("350x300")

        # list for showing habits
        self._habit_list = tk.Listbox(self._root, height=10, width=40)
        self._habit_list.pack(pady=15)

        # form for adding new habits
        form_frame = tk.Frame(self._root)
        form_frame.pack()

        # habit name input
        tk.Label(form_frame, text="Habit name").grid(row=0, column=0)
        self._name_input = tk.Entry(form_frame)
        self._name_input.grid(row=0, column=1)

        # habit description input
        tk.Label(form_frame, text="Description").grid(row=1, column=0)
        self._desc_input = tk.Entry(form_frame)
        self._desc_input.grid(row=1, column=1)

        # habit add button
        tk.Button(self._root, text="Add Habit", command=self._add_habit).pack(pady=10)

        self._reload_habits()

    def _reload_habits(self):
        self._habit_list.delete(0, tk.END)
        habits = self._habit_service.get_all()
        for habit in habits:
            self._habit_list.insert(tk.END, f"{habit.name} - {habit.description}")

    def _add_habit(self):
        name = self._name_input.get().strip()
        desc = self._desc_input.get().strip()

        habit_data = {
            "name": name,
            "description": desc,
        }

        if not name:
            messagebox.showerror("Error", "Name required")
            return

        try:
            self._habit_service.add(habit_data)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        self._name_input.delete(0, tk.END)
        self._desc_input.delete(0, tk.END)
        self._reload_habits()

    def run(self):
        self._root.mainloop()
