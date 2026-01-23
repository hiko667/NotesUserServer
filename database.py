import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()
polecenie = ""
c.execute(f"INSERT INTO users (id, username, password, token) VALUES (?, ?, ?, ?)", (0, "nexus", "super_secure", "17682096973829nexus"))
conn.commit()
c.close()
conn.close()

#INSERT INTO account (name, balance, transactions) VALUES ('Paweł', 1000.0, 99);
