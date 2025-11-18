import tkinter as tk
from tkinter import messagebox

class Interface:

    def __init__(self, root: Tk, habit_service: HabitService):
        self.habit_service = habit_service

        root.title("indolent")
        root.geometry("350x300")

        # list of all habits
        self.habit_list = tk.Listbox(root, height=10, width=40)
        self.habit_list.pack(pady=10)

        # form for adding new habits
        form_frame = tk.Frame(root)
        form_frame.pack()

        tk.Label(form_frame, text="Habit name").grid(row=0, column=0)
        self.name_entry = tk.Entry(form_frame)
        self.name_entry.grid(row=0, column=1)

        tk.Label(form_frame, text="Description").grid(row=1, column=0)
        self.desc_entry = tk.Entry(form_frame)
        self.desc_entry.grid(row=1, column=1)

        tk.Button(root, text="Add Habit", command=self.add_habit).pack(pady=10)

        self.refresh_list()

    def refresh_list(self):
        self.habit_list.delete(0, tk.END)
        habits = self.habit_service.list()
        for habit in habits:
            self.habit_list.insert(tk.END, f"{habit.name} — {habit.description}")

    def add_habit(self):
        name = self.name_entry.get().strip()
        desc = self.desc_entry.get().strip()

        if not name:
            messagebox.showerror("Error", "Name required")
            return

        try:
            self.habit_service.add(name, desc)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        self.name_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.refresh_list()