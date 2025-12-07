import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()
polecenie = ""
while polecenie != "exit":
    c.execute(polecenie)
    polecenie = input()
conn.commit()
c.close()
conn.close()

#INSERT INTO account (name, balance, transactions) VALUES ('Paweł', 1000.0, 99);
