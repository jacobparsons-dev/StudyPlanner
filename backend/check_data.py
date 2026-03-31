import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "study_optimiser.db"

print("CHECKING DB:", DB_PATH)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM study_items")
count = cursor.fetchone()[0]
print("study_items count:", count)

cursor.execute("SELECT item_id, subject, topic, question FROM study_items LIMIT 5")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()