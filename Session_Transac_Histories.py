import tkinter as tk
from tkinter import Frame, ttk
import mysql.connector
from Final_Admin_LandingPage import Admin_Page




class Session_Transaction_Histories:
  def __init__(self):
      self.employee = Admin_Page()

  def connect_to_database(self):
      connection = None
      try:
          host = "localhost"
          username = "root"
          password = ""
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

  def configure_style(self):
      style = ttk.Style()
      style.theme_use("clam")

      style.configure("Treeview",
                      background="white",
                      foreground="black",
                      rowheight=34,
                      fieldbackground="white",
                      font=("Arial", 10))

      style.configure("Treeview.Heading",
                      font=("Helvetica Bold", 12),
                      background="#3498db",
                      foreground="white")

      style.map("Treeview",
                background=[('selected', '#3498db')])

  def create_treeview_with_scrollbar(self, window, columns, headings):
      table_frame = Frame(window)
      table_frame.grid(row=1, column=0, padx=580, pady=355)

      treeview = ttk.Treeview(table_frame, columns=columns, show="headings")
      scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=treeview.yview)
      treeview.configure(yscrollcommand=scrollbar.set)

      for col, head in zip(columns, headings):
          treeview.column(col, width=180, anchor="center")
          treeview.heading(col, text=head)

      treeview.pack(side="left", fill="y")
      scrollbar.pack(side="right", fill="y")

      return treeview

  def populate_treeview(self, treeview, query, column_count):
      connection = self.connect_to_database()
      cursor = connection.cursor()
      cursor.execute(query)
      rows = cursor.fetchall()

      for row in rows:
          treeview.insert("", 'end', values=row[:column_count])

  def transactions(self, parent_window):
    #   window = Frame(parent_window)

    #   window.title("Transaction Records")

      self.configure_style()

      columns = ("transactions_id", "transaction_type", "receiving_account", "transaction_date", "amount")
      headings = ("Transaction ID", "Transaction Type", "Receiving Account", "Transaction Date", "Amount")

      trv = self.create_treeview_with_scrollbar(parent_window, columns, headings)
      query = "SELECT transactions_id, checkings_id, transaction_type, receiving_account, transaction_date, amount FROM transactions"
      self.populate_treeview(trv, query, len(columns))
      
      
  def customer_checkings_view(self, connection, parent_window, employee_id):
    #   window = Frame(parent_window)

    #   window.title("Transaction Records")

      self.configure_style()

      columns = ("customer_id", "customer_name", "email", "address", "id_type", "occupation", "annual_gross_income", "checkings_id", "account_password", "balance", "account_status")
      headings = ("CustomerID", "CustomerName", "Email", "Address", "IDType", "Occupation", "AnnualGrossIncome", "CheckingsID", "AccountPassword", "Balance", "AccountStatus")

      trv = self.create_treeview_with_scrollbar(parent_window, columns, headings)
      query = "SELECT * FROM customer_checkings_view"
      self.populate_treeview(trv, query, len(columns))
      self.employee.add_transaction_log(connection, employee_id, "View User", "customer_information", None, None, None)
    #   window.mainloop()

  # def customer_account_records(self):
  #     window = tk.Tk()
  #     window.geometry('1200x600')
  #     window.title("Customer Records")

  #     self.configure_style()

  #     columns = ("customer_id", "customer_name", "email", "address", "id_type", "occupation",
  #               "annual_gross_income", "checkings_id", "account_password", "balance", "account_status")
  #     headings = ("Customer ID", "Customer Name", "Email", "Address", "ID Type", "Occupation",
  #                 "Annual Gross Income", "Checkings ID", "Account Password", "Balance", "Account Status")

  #     trv = self.create_treeview_with_scrollbar(window, columns, headings)
  #     query = '''
  #         SELECT
  #             c.customer_id, CONCAT(c.first_name, ' ', c.last_name) AS customer_name, c.email, c.address,
  #             c.id_type, c.occupation, c.annual_gross_income, ca.checkings_id, ca.account_password,
  #             ca.balance, ca.account_status
  #         FROM
  #             customer_information c
  #         JOIN
  #             checkings_account ca ON c.customer_id = ca.customer_id
  #     '''
  #     self.populate_treeview(trv, query, len(columns))

  #     window.mainloop()


# treeviewss = Session_Transaction_Histories()
# treeviewss.transactions()
