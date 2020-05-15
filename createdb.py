## ONLY RUN FOR SQLite3 USE

import sqlite3

conn = sqlite3.connect('employee.db')

c = conn.cursor()

c.execute("CREATE TABLE employees (first text, last text, pay integer)")

c.execute("INSERT INTO employees VALUES ('Chris', 'Hein', 100000)")
c.execute("INSERT INTO employees VALUES ('Alex', 'Hein', 50000)")
c.execute("INSERT INTO employees VALUES ('Bob', 'Saget', 1000)")

conn.commit()

c.execute("SELECT * FROM employees")

print(c.fetchall())

conn.close()
