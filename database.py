import sqlite3
from ExpenseRecord import ExpenseRecord

DB_NAME = "expenses.db"

def init_db():
    """Creates the expenses table if it does not already exist"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL,
            category TEXT,
            description TEXT,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_expense_to_db(record: ExpenseRecord):
    """Inserts a validated ExpenseRecord into the database"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO expenses(amount,category,description,date)VALUES(?,?,?,?)",
        (record.amount, record.category, record.description, record.date)
    )
    conn.commit()
    conn.close()