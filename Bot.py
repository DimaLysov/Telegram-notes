import telebot
import sqlite3
import os

bot = telebot.TeleBot("8080539230:AAH7x2vQ2wBmvnUKhGnOVQlrptn4sjlnWXs")
now_family = ''
now_user_id = ''


def view_info(name_table):
    global now_family
    conn = sqlite3.connect(f'{now_family}.sql')
    cur = conn.cursor()
    cur.execute("select * from %s" % name_table)
    info = cur.fetchall()
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
                        surname text
                        )''')
    conn.commit()
    cor.execute('''create table if not exists list_notes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        family_id int,
                        notes text not null,
                        date timestamp,
                        foreign key (family_id) references list_family(id)
                        )''')
    conn.commit()
    cor.close()
    conn.close()


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Добро пожаловать')

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Список команд которые могут вам понадобиться:\n'
                                      '/create_family - Создать семью\n'
                                      '/choice_family - Сменить семью\n'
                                      '/add_person - Добавить человека в семью\n'
                                      '/add_note - Добавить событие для человека\n'
                                      '/view_family - Показать состав семьи\n'
                                      '/view_notes - Показать события семьи\n'
                                      '/now_family - Показать выбранную семью\n')


@bot.message_handler(commands=['create_family'])
def accept_family_name(message):
    bot.send_message(message.chat.id, 'Ведите название своей семьи')
    bot.register_next_step_handler(message, create_family)


def create_family(message):
    global now_family
    now_family = message.text.strip()
    if os.path.exists(f'{now_family}.sql'):
        bot.send_message(message.chat.id, 'Данная семья уже существуют')
        return
    for i in '<>:"/\|?*':
        if i in now_family:
            bot.send_message(message.chat.id, 'Название семьи не может включать данные символы:\n< > : " / \ | ? *')
            return
    new_family(now_family)
    bot.send_message(message.chat.id, 'Вы успешно перешли в вашу новую семью')


@bot.message_handler(commands=['choice_family'])
def accept_family(message):
    bot.send_message(message.chat.id, 'Введите семью в которую хотите перейти')
    bot.register_next_step_handler(message, choice_family)


def choice_family(message):
    global now_family
    if os.path.exists(f'{message.text}.sql'):
        now_family = message.text.strip()
        bot.send_message(message.chat.id, 'Вы успешно перешли в вашу семью')
    else:
        bot.send_message(message.chat.id, 'Такой семьи не существует')

@bot.message_handler(commands=['add_person'])
def accept_person(message):
    global now_family
    if now_family == '':
        bot.send_message(message.chat.id, 'Нельзя добавить человека, пока не выбрана семья')
        return
    bot.send_message(message.chat.id, 'Введите имя и фамилию нового человека через пробел')
    bot.register_next_step_handler(message, add_person)


def add_person(message):
    global now_family
    if len(message.text.strip().split()) != 2:
        bot.send_message(message.chat.id, 'Данные введены не корректно, попробуйте снова')
        bot.register_next_step_handler(message, add_person)
    name, surname = message.text.strip().split()
    conn = sqlite3.connect(f'{now_family}.sql')
    cur = conn.cursor()
    cur.execute("insert into list_family (name, surname) values ('%s', '%s')" % (name, surname))
    conn.commit()
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, 'Вы успешно добавили человека')


@bot.message_handler(commands=['add_note'])
def accept_user(message):
    global now_family
    if now_family == '':
        bot.send_message(message.chat.id, 'Нельзя добавить событие, пока не выбрана семья')
        return
    bot.send_message(message.chat.id, 'Введите имя и фамилию человека, для которого хотите добавить событие')
    bot.register_next_step_handler(message, accept_id_user)


def accept_id_user(message):
    global now_family, now_user_id
    if len(message.text.strip().split()) != 2:
        bot.send_message(message.chat.id, 'Данные введены не корректно, попробуйте снова')
        bot.register_next_step_handler(message, accept_id_user)
    name, surname = message.text.strip().split()
    conn = sqlite3.connect(f'{now_family}.sql')
    cur = conn.cursor()
    cur.execute("select id from list_family where name = '%s' and surname = '%s'" % (name, surname))
    now_user_id = cur.fetchone()
    if now_user_id is None:
        bot.send_message(message.chat.id, 'Данного человека нет в семье')
        return
    now_user_id = now_user_id[0]
    bot.send_message(message.chat.id, 'Введите дату и само событие в формате:\ndate(day.month.year)_note')
    bot.register_next_step_handler(message, add_note)


def add_note(message):
    global now_family, now_user_id
    if len(message.text.strip().split('_')) != 2:
        bot.send_message(message.chat.id, 'Не корректно введены данные, попробуйте снова')
        bot.register_next_step_handler(message, add_note)
    date, note = message.text.strip().split('_')
    conn = sqlite3.connect(f'{now_family}.sql')
    cur = conn.cursor()
    cur.execute("insert into list_notes (family_id, notes, date) values ('%s', '%s', '%s')" % (now_user_id, note, date))
    conn.commit()
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, 'Вы успешно добавли событие')


@bot.message_handler(commands=['view_notes'])
def view_notes(message):
    global now_family
    if now_family == '':
        bot.send_message(message.chat.id, 'В данный момент семья не выбрана')
        return
    notes = view_info('list_notes')
    print(notes)
    conn = sqlite3.connect(f'{now_family}.sql')
    cur = conn.cursor()
    info = f'Список событий семьи {now_family}:\n'
    for note in notes:
        cur.execute("select name, surname from list_family where id=%s" % note[1])
        name, surname = cur.fetchone()
        info += f'{name} {surname}: {note[2]}. Дата {note[3]}\n'
    bot.send_message(message.chat.id, info)


@bot.message_handler(commands=['view_family'])
def view_family(message):
    global now_family
    if now_family == '':
        bot.send_message(message.chat.id, 'В данный момент семья не выбрана')
        return
    persons = view_info('list_family')
    info = f'Список семьи {now_family}:\n'
    for person in persons:
        info += f'{person[1]} {person[2]}\n'
    bot.send_message(message.chat.id, info)


@bot.message_handler(commands=['now_family'])
def write_now_family(message):
    global now_family
    answer = f'Выбрана семья: {now_family}' if now_family != '' else 'В данный момент семья не выбрана'
    bot.send_message(message.chat.id, answer)


bot.infinity_polling()
