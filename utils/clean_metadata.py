import sqlite3

db_path = "metadata.db"
conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.execute("DELETE FROM ebooks WHERE title LIKE 'testxy%'")
conn.commit()
conn.close()

print("Deleted rows where title starts with 'testxy'.")