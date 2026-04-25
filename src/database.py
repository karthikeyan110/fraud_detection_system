import sqlite3
import os

# Create DB path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "transactions.db")


# -----------------------------
# Create table (run once)
# -----------------------------
def create_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Time REAL,
        Amount REAL,
        fraud_score REAL,
        label TEXT
    )
    """)

    conn.commit()
    conn.close()


# -----------------------------
# Insert transaction
# -----------------------------
def insert_transaction(data, score, label):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO transactions (Time, Amount, fraud_score, label)
    VALUES (?, ?, ?, ?)
    """, (
        data["Time"],
        data["Amount"],
        score,
        label
    ))

    conn.commit()
    conn.close()


# -----------------------------
# Fetch all data
# -----------------------------
def get_all_transactions():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM transactions")
    rows = cursor.fetchall()

    conn.close()
    return rows