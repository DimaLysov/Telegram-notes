import telebot
import sqlite3
import os

bot = telebot.TeleBot("8080539230:AAH7x2vQ2wBmvnUKhGnOVQlrptn4sjlnWXs")
now_family = ''


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Добро пожаловать')


@bot.message_handler(commands=['create_family'])
def accept_family_name(message):
    bot.send_message(message.chat.id, 'Ведите название своей семьи')
    bot.register_next_step_handler(message, create_family)


def create_family(message):
    global now_family
    name_family = message.text.strip()
    new_family = open(f'{name_family}.sql', 'w')
    new_family.close()
    now_family = name_family
    conn = sqlite3.connect(f'{now_family}.sql')
    cor = conn.cursor()
    cor.execute(
        "create table if not exists list_family (id int avto_increment primary key, name varchar(50), surname varchar(50))")
    conn.commit()
    cor.close()
    conn.close()
    now_family = name_family
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
        bot.send_message(message.chat.id, 'Такой семьи не существует, поробуйте снова')
        bot.register_next_step_handler(message, choice_family)


@bot.message_handler(commands=['add_person'])
def accept_person(message):
    bot.send_message(message.chat.id, 'Введите имя и фамилию нового человека через пробел')
    bot.register_next_step_handler(message, add_person)


def add_person(message):
    global now_family
    name, surname = message.text.strip().split()
    conn = sqlite3.connect(f'{now_family}.sql')
    cur = conn.cursor()
    cur.execute("insert into list_family (name, surname) values ('%s', '%s')" % (name, surname))
    conn.commit()
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, 'Вы успешно добавили человека')


@bot.message_handler(commands=['view_family'])
def view_family(message):
    global now_family
    conn = sqlite3.connect(f'{now_family}.sql')
    cur = conn.cursor()
    cur.execute('select * from list_family')
    persons = cur.fetchall()
    info = f'Список семьи {now_family}:\n'
    for person in persons:
        info += f'Имя: {person[1]}, фамилия: {person[2]}\n'
    bot.send_message(message.chat.id, info)


@bot.message_handler(commands=['now_family'])
def write_now_family(message):
    global now_family
    answer = f'Выбрана семья: {now_family}' if now_family != '' else 'В данный момент семья не выбрана'
    bot.send_message(message.chat.id, answer)


bot.infinity_polling()
