from Employee import Employee
from Customer import Customer
from BankingMethods import BankingMethods
from tkinter import messagebox
from tabulate import tabulate
from datetime import datetime
import os
import tkinter as tk

def line_printer():
    for x in range(100):
        print("=", end = "")

while True:
    line_printer()
    print("\n                                          Treasury Citadel")
    line_printer()
    print("\n\nWelcome to Trasury Citadel. How may we serve you today?")
    print("[1] Log in as Employee")
    print("[2] Log in as Customer")
    print("[3] Exit Program")

    choice = input("\nEnter your choice (1, 2, or 3): ")

    if choice == '1':
        print(1)
        object1 = Employee()
        object1.connect()
        object1.login_page()

    elif choice == '2':
        print(2)
        object2 = Customer()
        object2.connect()
        object2.login_page()

    elif choice == '3':
        os.system("cls")
        line_printer()
        print("\n                                          Treasury Citadel")
        line_printer()
        print("\nThank you for using the program. Goodbye!")
        break
    else:
        print("Invalid input. Please enter 1, 2, or 3.")