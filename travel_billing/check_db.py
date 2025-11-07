import sqlite3

conn = sqlite3.connect("travel_billing.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM bills")
rows = cursor.fetchall()

print("🧾 All Bills in Database:")
for row in rows:
    print(row)

conn.close()
