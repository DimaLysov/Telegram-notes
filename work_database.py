import sqlite3

def view_info(name_table, family):
    conn = sqlite3.connect(f'{family}.sql')
    cur = conn.cursor()
    cur.execute("select * from %s" % name_table)
    info = cur.fetchall()
    cur.close()
    conn.close()
    print(info)
    return info

def new_family(name_family):
    fail = open(f'{name_family}.sql', 'w')
    fail.close()
    conn = sqlite3.connect(f'{name_family}.sql')
    cor = conn.cursor()
    cor.execute('''create table if not exists list_family (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name text not null,
                        surname text
                        )''')
    conn.commit()
    cor.execute('''create table if not exists list_notes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        family_id int,
                        notes text not null,
                        date_start text,
                        date_end text,
                        time_start text,
                        time_end text,
                        foreign key (family_id) references list_family(id)
                        )''')
    conn.commit()
    cor.close()
    conn.close()


def new_person(name, surname, family):
    conn = sqlite3.connect(f'{family}.sql')
    cur = conn.cursor()
    cur.execute("insert into list_family (name, surname) values ('%s', '%s')" % (name, surname))
    conn.commit()
    cur.close()
    conn.close()

def new_note(user_id, note, start_date, end_date, start_time, end_time, family):
    conn = sqlite3.connect(f'{family}.sql')
    cur = conn.cursor()
    cur.execute("insert into list_notes (family_id, notes, date_start, date_end, time_start, time_end)"
                " values (%s, '%s', '%s', '%s', '%s', '%s')" % (
                    user_id, note, start_date, end_date, start_time, end_time))
    conn.commit()
    cur.close()
    conn.close()

def select_id(name, surname, family):
    conn = sqlite3.connect(f'{family}.sql')
    cur = conn.cursor()
    cur.execute("select id from list_family where name = '%s' and surname = '%s'" % (name, surname))
    return cur.fetchone()