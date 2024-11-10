import sqlite3


def view_info(name_table, family):
    conn = sqlite3.connect(f'{family}.sql')
    cur = conn.cursor()
    cur.execute("select * from %s" % name_table)
    info = cur.fetchall()
    print(info)
    cur.close()
    conn.close()
    return info


def new_family(name_family):
    fail = open(f'{name_family}.sql', 'w')
    fail.close()
    conn = sqlite3.connect(f'{name_family}.sql')
    cor = conn.cursor()
    cor.execute('''create table if not exists list_family (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name text not null,
                        surname text,
                        tag text,
                        chat_id int
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


def new_person(name, surname, tag, chat_id, family):
    conn = sqlite3.connect(f'{family}.sql')
    cur = conn.cursor()
    cur.execute("insert into list_family (name, surname, tag, chat_id)"
                "values ('%s', '%s', '%s', '%s')" % (name, surname, tag, chat_id))
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
    answer = cur.fetchall()
    print(answer)
    cur.close()
    conn.close()
    return answer


def check_human_being(tag, family):
    conn = sqlite3.connect(f'{family}.sql')
    cur = conn.cursor()
    cur.execute("select tag from list_family where tag = '%s'" % tag)
    answer = cur.fetchone()
    cur.close()
    conn.close()
    return answer


def update_user_id(chat_id, tag, family):
    conn = sqlite3.connect(f'{family}.sql')
    cur = conn.cursor()
    cur.execute("update list_family set chat_id = '%s' where tag = '%s'" % (chat_id, tag))
    conn.commit()
    cur.close()
    conn.close()


def uppdate_id_family(chat_id, family):
    conn = sqlite3.connect('id_chosen_family.sql')
    cur = conn.cursor()
    cur.execute("select chat_id from id_family where chat_id = '%s'" % chat_id)
    user = cur.fetchone()
    if user is None:
        cur.execute("insert into id_family (chat_id, family)"
                    "values ('%s', '%s')" % (chat_id, family))
        conn.commit()
    else:
        cur.execute("update id_family set family = '%s' where chat_id = '%s'" % (family, chat_id))
        conn.commit()
    cur.close()
    conn.close()


def get_family(chat_id):
    conn = sqlite3.connect('id_chosen_family.sql')
    cur = conn.cursor()
    cur.execute("select family from id_family where chat_id = '%s'" % chat_id)
    answer = cur.fetchone()
    print(answer)
    cur.close()
    conn.close()
    if answer is None:
        return 'null'
    return answer[0]