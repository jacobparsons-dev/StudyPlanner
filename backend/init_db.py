import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "study_optimiser.db"

def main():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute(""" 
                   CREATE TABLE IF NOT EXISTS study_items (
                   item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   subject TEXT NOT NULL,
                   topic TEXT NOT NULL,
                   question TEXT NOT NULL,
                   answer TEXT NOT NULL,
                   difficulty INTEGER DEFAULT 3,
                   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                   )
                   """)
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS reviews (
                   review_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   item_id INTEGER NOT NULL,
                   timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                   correct INTEGER NOT NULL,
                   confidence INTEGER NOT NULL,
                   response_time REAL NOT NULL,
                   FOREIGN KEY (item_id) REFERENCES study_items(item_id)
                   )
                   """)
    connection.commit()
    connection.close()
    print(f"Database created at: {DB_PATH}")
if __name__ == "__main__":
    main()