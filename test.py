import sqlite3
number = 1
conn = sqlite3.connect('Himiki.sql')
cur = conn.cursor()
cur.execute("select name, surname from list_family where id=%s" % number)
name, surname = cur.fetchone()
print(name, surname)
cur.close()
conn.close()