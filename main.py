import psycopg2

conn = psycopg2.connect(dbname="Test", user="postgres", password="2312", port="5432")
cur = conn.cursor()
# cur.execute(
#     "create table family (id serial primary key, FirstName character varying(30), SecondName character varying(30))")
name = input("Введите имя пользователя: ")
surname = input("Введите фамилию пользователя: ")
cur.execute(f"insert into family (firstname, lastname) values ('{name}', '{surname}')")
conn.commit()
cur.execute("select * from family")
print(cur.fetchall())
cur.close()
conn.close()
# CREATE TABLE Family
# (
# 	Id SERIAL PRIMARY KEY,
#     firstname character varying(30),
#     lastname character varying(30)
# );
