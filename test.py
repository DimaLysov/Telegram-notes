import sqlite3
from work_database import get_family
name = 'Дмитрий'
surname = 'Лысов'
a = get_family(88544849)
# cur.execute('''create table if not exists id_family (
#                         id INTEGER PRIMARY KEY AUTOINCREMENT,
#                         chat_id int not null,
#                         family text
#                         )''')
print(a)
#885444849
#id_chosen_family