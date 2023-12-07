import calendar
import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar, DateEntry

class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Calendar")
        self.selected_date_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        # Calendar
        cal_label = ttk.Label(self.root, text="Select a Date:")
        cal_label.grid(row=0, column=0, padx=10, pady=10)
        self.calendar = DateEntry(self.root, width=12, background="darkblue", foreground="white", borderwidth=2)
        self.calendar.grid(row=0, column=1, padx=10, pady=10)

        # Show Calendar Button
        show_button = ttk.Button(self.root, text="Show Calendar", command=self.show_calendar)
        show_button.grid(row=1, column=0, columnspan=2, pady=10)

        # Selected Date Label
        selected_date_label = ttk.Label(self.root, text="Selected Date:")
        selected_date_label.grid(row=2, column=0, pady=10)
        selected_date_display = ttk.Label(self.root, textvariable=self.selected_date_var)
        selected_date_display.grid(row=2, column=1, pady=10)

    def show_calendar(self):
        selected_date = self.calendar.get()
        self.selected_date_var.set(selected_date)

if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarApp(root)
    root.mainloop()
