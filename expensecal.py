import tkinter as tk
from tkinter import messagebox
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("400x300")

        # Create database connection
        self.conn = sqlite3.connect("expenses.db")
        self.cursor = self.conn.cursor()

        # Create tables if they don't exist
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY,
                date TEXT,
                amount REAL,
                category TEXT
            )
        """)

        # Create GUI components
        self.category_var = tk.StringVar(self.root)
        self.category_var.set("Food")

        self.expense_frame = tk.Frame(self.root)
        self.expense_frame.pack(fill="x")

        self.expense_label = tk.Label(self.expense_frame, text="Expense:")
        self.expense_label.pack(side="left")

        self.expense_entry = tk.Entry(self.expense_frame)
        self.expense_entry.pack(side="left")

        self.category_label = tk.Label(self.expense_frame, text="Category:")
        self.category_label.pack(side="left")

        self.category_menu = tk.OptionMenu(self.expense_frame, self.category_var, "Food", "Entertainment", "Clothing")
        self.category_menu.pack(side="left")

        self.expense_button = tk.Button(self.expense_frame, text="Add", command=self.add_expense)
        self.expense_button.pack(side="left")

        self.report_button = tk.Button(self.root, text="Generate Report", command=self.generate_report)
        self.report_button.pack(fill="x")

    def add_expense(self):
        amount = self.expense_entry.get()
        if amount:
            category = self.category_var.get()
            self.cursor.execute("INSERT INTO expenses (date, amount, category) VALUES (?,?,?)",
                                (datetime.now().strftime("%Y-%m-%d"), float(amount), category))
            self.conn.commit()
            self.expense_entry.delete(0, "end")

    def generate_report(self):
        # Get data from database
        self.cursor.execute("SELECT date, amount, category FROM expenses")
        expense_data = self.cursor.fetchall()

        # Create plots
        categories = ["Food", "Entertainment", "Clothing"]
        amounts = [0, 0, 0]
        for entry in expense_data:
            if entry[2] == "Food":
                amounts[0] += entry[1]
            elif entry[2] == "Entertainment":
                amounts[1] += entry[1]
            elif entry[2] == "Clothing":
                amounts[2] += entry[1]

        fig, ax = plt.subplots()
        ax.pie(amounts, labels=categories)
        ax.axis("equal")
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
