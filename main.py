import sqlite3
from datetime import datetime
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

DB = "expenses.db"

class ExpensePredictor:
    def __init__(self):
        self.conn = sqlite3.connect(DB)
        self.create_table()

    def create_table(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL,
            category TEXT,
            date TEXT
        )
        """)
        self.conn.commit()

    def add_expense(self, amount, category):
        date = datetime.now().strftime("%Y-%m-%d")
        self.conn.execute(
            "INSERT INTO expenses (amount, category, date) VALUES (?, ?, ?)",
            (amount, category, date)
        )
        self.conn.commit()

    def get_data(self):
        df = pd.read_sql_query("SELECT * FROM expenses", self.conn)
        return df

    def analyze(self):
        df = self.get_data()
        if df.empty:
            print("No data available")
            return

        total = df["amount"].sum()
        print("\nTotal Spending:", total)

        print("\nCategory Breakdown:")
        print(df.groupby("category")["amount"].sum())

    def predict(self):
        df = self.get_data()
        if len(df) < 5:
            print("Not enough data for prediction")
            return

        df["day"] = range(len(df))

        X = df[["day"]]
        y = df["amount"]

        model = LinearRegression()
        model.fit(X, y)

        next_day = np.array([[len(df)]])
        prediction = model.predict(next_day)[0]

        print("\nPredicted next expense:", round(prediction, 2))

        avg = y.mean()
        if prediction > avg * 1.5:
            print("Warning: Possible overspending ahead!")

def main():
    tracker = ExpensePredictor()

    while True:
        print("\n1. Add Expense")
        print("2. Analyze Spending")
        print("3. Predict Future Expense")
        print("4. Exit")

        choice = input("Choose: ")

        if choice == "1":
            amount = float(input("Amount: "))
            category = input("Category: ")
            tracker.add_expense(amount, category)
            print("Expense added")

        elif choice == "2":
            tracker.analyze()

        elif choice == "3":
            tracker.predict()

        elif choice == "4":
            break

        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
