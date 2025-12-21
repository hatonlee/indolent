import tkinter as tk


class ActionBar(tk.Frame):
    def __init__(self, parent: tk.Misc, open_create_window_cb):
        super().__init__(parent)
        self._open_create_window_cb = open_create_window_cb
        self._render()

    def _render(self):
        self.actions_frame = tk.Frame(self, bg="grey", padx=5, pady=5)
        self.actions_frame.grid(row=0, column=0, columnspan=1, sticky="ew")
        self.actions_frame.columnconfigure(1, weight=1)

        self._render_create_button()
        self._render_view_buttons()

    def _render_create_button(self):
        create_button = tk.Button(
            self.actions_frame,
            text="Create Habit",
            command=self._open_create_window_cb,
            bg="grey",
            fg="white",
        )
        create_button.grid(row=0, column=0, padx=5, pady=5)

    def _render_view_buttons(self):
        self.view_buttons_frame = tk.Frame(self.actions_frame, bg="grey")
        self.view_buttons_frame.grid(row=0, column=1, sticky="e")

        self._render_daily_button()
        self._render_weekly_button()
        self._render_monthly_button()

    def _render_daily_button(self):
        daily_button = tk.Button(
            self.view_buttons_frame,
            text="Daily View",
            bg="grey",
            fg="white",
        )
        daily_button.grid(row=0, column=0, padx=5, pady=5, sticky="e")

    def _render_weekly_button(self):
        weekly_button = tk.Button(
            self.view_buttons_frame,
            text="Weekly View",
            bg="grey",
            fg="white",
        )
        weekly_button.grid(row=0, column=1, padx=5, pady=5)

    def _render_monthly_button(self):
        monthly_button = tk.Button(
            self.view_buttons_frame,
            text="Monthly View",
            bg="grey",
            fg="white",
        )
        monthly_button.grid(row=0, column=2, padx=5, pady=5)
