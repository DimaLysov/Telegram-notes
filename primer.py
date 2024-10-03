import telebot
import sqlite3
import requests
import json

bot = telebot.TeleBot("8080539230:AAH7x2vQ2wBmvnUKhGnOVQlrptn4sjlnWXs")
api = '44b3502f8bfc5ba8336eeb0ae3724621'


@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('database.sql')
    cur = conn.cursor()
    cur.execute(
        'create table if not exists users (id int avto_increment primary key, name varchar(50), pass varchar(50))')
    conn.commit()
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, 'Добро пожаловать')


@bot.message_handler(commands=['weather'])
def weather(message):
    bot.send_message(message.chat.id, 'Введите название города, в котором хотите узнать температуру')
    bot.register_next_step_handler(message, city_temp)


def city_temp(message):
    city = message.text.strip().lower()
    temp = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api}&units=metric')
    if temp.status_code == 200:
        data = json.loads(temp.text)
        bot.reply_to(message, f'Сейчас погода: {data["main"]["temp"]} градусов')
    else:
        bot.send_message(message.chat.id, 'Город указан не корректно, повторите попытку')
        bot.register_next_step_handler(message, city_temp)


@bot.message_handler(commands=['new_person'])
def new_person(message):
    bot.send_message(message.chat.id, 'Введите имя и пароль в данном фромате:\nuser_password')
    bot.register_next_step_handler(message, registration)


def registration(message):
    name, password = str(message.text.strip()).split('_')
    conn = sqlite3.connect('database.sql')
    cur = conn.cursor()
    cur.execute("insert into users (name, pass) values ('%s', '%s')" % (name, password))
    conn.commit()
    cur.close()
    conn.close()
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Список пользователей', callback_data='users'))
    bot.send_message(message.chat.id, 'Пользователь зарегестрирован', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    conn = sqlite3.connect('database.sql')
    cur = conn.cursor()
    cur.execute("select * from users")
    users = cur.fetchall()
    info = ''
    for el in users:
        info += f'Имя: {el[1]}, пароль: {el[2]}\n'
    cur.close()
    conn.close()
    bot.send_message(call.message.chat.id, info)


bot.infinity_polling()
