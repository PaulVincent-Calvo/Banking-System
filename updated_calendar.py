import tkinter as tk
from tkcalendar import Calendar

class CalendarGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Calendar GUI")

        self.cal = Calendar(self.root, selectmode="day", year=2023, month=11, day=27)
        self.cal.pack(pady=20)

        self.get_date_button = tk.Button(self.root, text="Get Selected Date", command=self.get_selected_date)
        self.get_date_button.pack(pady=10)

    def get_selected_date(self):
        selected_date = self.cal.get_date()
        print(f"Selected Date: {selected_date}")
        self.root.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    calendar_gui = CalendarGUI()
    calendar_gui.run()
