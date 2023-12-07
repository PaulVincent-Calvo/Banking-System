import tkinter as tk
from tkinter import ttk
import mysql.connector

def connect_to_database():
    connection = None
    try:
        host = "192.168.1.134"
        username = "user_treasury_citadel"
        password = "tC23_oop_dbms_pRoj2023"
        database = "treasury_citadel_database"

        connection = mysql.connector.connect(
            host=host,
            user=username,
            password=password,
            database=database
        )

        print("Database Initialization Successful...")

    except mysql.connector.Error as error:
        print(error)

    return connection

def configure_style():
    style = ttk.Style()
    style.theme_use("clam")

    style.configure("Treeview",
                    background="white",
                    foreground="black",
                    rowheight=25,
                    fieldbackground="white",
                    font=("Arial", 10))

    style.configure("Treeview.Heading",
                    font=("Helvetica Bold", 10),
                    background="#3498db",
                    foreground="white")

    style.map("Treeview",
              background=[('selected', '#3498db')])

def create_treeview_with_scrollbar(window, columns, headings):
    frame = ttk.Frame(window)
    frame.grid(row=1, column=0, padx=20, pady=20)

    treeview = ttk.Treeview(frame, columns=columns, show="headings")
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=treeview.yview)
    treeview.configure(yscrollcommand=scrollbar.set)

    for col, head in zip(columns, headings):
        treeview.column(col, width=100, anchor="center")
        treeview.heading(col, text=head)

    treeview.pack(side="left", fill="y")
    scrollbar.pack(side="right", fill="y")

    return treeview

def populate_treeview(treeview, query, column_count):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()

    for row in rows:
        treeview.insert("", 'end', values=row[:column_count])

def sessions():
    window = tk.Tk()
    window.geometry('1150x350')
    window.title("Session Logs")

    configure_style()

    columns = ("session_log_id", "employee_id", "session_date", "session_type", "table_involved", "column_involved", "modified_value", "stored_value", "status", "last_modified", "version")
    headings = ("Session ID", "Employee ID", "Session Date", "Session Type", "Table Involved", "Column Involved", "Modified Value", "Stored Value", "Status", "Last Modified", "Version")

    trv = create_treeview_with_scrollbar(window, columns, headings)
    query = "SELECT session_log_id, employee_id, session_date, session_type, table_involved, column_involved, modified_value, stored_value, status, last_modified, version  amount FROM session_log"
    populate_treeview(trv, query, len(columns))

    window.mainloop()


sessions()
