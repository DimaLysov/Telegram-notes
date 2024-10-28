import telebot
from telebot import types
import os
from work_database import view_info, new_family, new_person, select_id, new_note, check_human_being, update_user_id
from functions import compare_dates, check_now_dates

bot = telebot.TeleBot("8080539230:AAH7x2vQ2wBmvnUKhGnOVQlrptn4sjlnWXs")
now_family, now_user_id, now_note, now_date = '', '', '', ''


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_1 = types.KeyboardButton('/create_family')
    btn_2 = types.KeyboardButton('/choice_family')
    markup.row(btn_1, btn_2)
    bot.send_message(message.chat.id, 'Добро пожаловать\n'
                                      'Создать новую семью или войдите в уже существующую', reply_markup=markup)


@bot.message_handler(commands=['help'])
def view_commands(message):
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
    bot.send_message(message.chat.id, 'Ведите название своей семьи', reply_markup=types.ReplyKeyboardRemove())
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
    bot.send_message(message.chat.id, 'Введите семью в которую хотите перейти',
                     reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, choice_family)


def choice_family(message):
    global now_family
    if os.path.exists(f'{message.text}.sql'):
        now_family = message.text.strip()
        check = check_human_being('@' + message.from_user.username, now_family)
        if check is None:
            now_family = ''
            bot.send_message(message.chat.id, 'Ваш тег не добавли в данную семью, поэтому вы не можете в нее зайти')
        else:
            update_user_id(message.from_user.id, '@' + message.from_user.username, now_family)
            bot.send_message(message.chat.id, 'Вы успешно перешли в вашу семью')
    else:
        bot.send_message(message.chat.id, 'Такой семьи не существует')


@bot.message_handler(commands=['add_person'])
def accept_person(message):
    global now_family
    if now_family == '':
        bot.send_message(message.chat.id, 'Нельзя добавить человека, пока не выбрана семья')
        return
    bot.send_message(message.chat.id, 'Введите имя, фамилию и тег нового человека через пробел\n'
                                      'Пример: Иван Иванович @ivan\n'
                                      'Если какого-то параметра нет введите вместо него -')
    bot.register_next_step_handler(message, add_person)


def add_person(message):
    global now_family
    if len(message.text.strip().split()) != 3:
        bot.send_message(message.chat.id, 'Данные введены не корректно, попробуйте снова')
        bot.register_next_step_handler(message, add_person)
        return
    human_data = message.text.strip()
    human_data = human_data.replace('-', 'Null')
    name, surname, tag = human_data.split()
    chat_id = 'Null'
    if tag[1:] == message.from_user.username:
        chat_id = message.from_user.id
    new_person(name, surname, tag, chat_id, now_family)
    bot.send_message(message.chat.id, 'Вы успешно добавили человека')


@bot.message_handler(commands=['add_note'])
def accept_user(message):
    global now_family
    if now_family == '':
        bot.send_message(message.chat.id, 'Нельзя добавить событие, пока не выбрана семья')
        return
    bot.send_message(message.chat.id, 'Введите имя и фамилию человека, для которого хотите добавить событие')
    bot.register_next_step_handler(message, accept_note)


def accept_note(message):
    global now_family, now_user_id
    if len(message.text.strip().split()) != 2:
        bot.send_message(message.chat.id, 'Данные введены не корректно, попробуйте снова')
        bot.register_next_step_handler(message, accept_note)
        return
    name, surname = message.text.strip().lower().split()
    now_user_id = select_id(name, surname, now_family)
    if now_user_id is None:
        bot.send_message(message.chat.id, 'Данного человека нет в семье')
        return
    now_user_id = now_user_id[0]
    bot.send_message(message.chat.id, 'Введите событие')
    bot.register_next_step_handler(message, accept_date)


def accept_date(message):
    global now_note
    if message.text.strip() == '':
        bot.send_message(message.chat.id, 'Вы не ввели событие, попробуйте снова')
        bot.register_next_step_handler(message, accept_date)
        return
    now_note = message.text.strip()
    bot.send_message(message.chat.id, 'Введите дату в формате:\n'
                                      'начало-конец\n'
                                      'Пример: 10.10.2024-11.11.2024\n'
                                      'Если какой-то даты нет, поставьте вместо нее *')
    bot.register_next_step_handler(message, accept_time)


def accept_time(message):
    global now_date
    now_date = message.text.strip()
    now_date = now_date.replace('*', 'Null')
    now_date = now_date.split('-')
    if len(now_date) != 2:
        bot.send_message(message.chat.id, 'Данные введены не корректно, попробуйте снова')
        bot.register_next_step_handler(message, accept_time)
        return
    elif compare_dates(now_date[0], now_date[1], "%d.%m.%Y"):
        bot.send_message(message.chat.id, 'Дата начала не может быть позже даты конца. Повторите снова')
        bot.register_next_step_handler(message, accept_time)
        return
    elif check_now_dates(now_date[0], "%d.%m.%Y") or check_now_dates(now_date[1], "%d.%m.%Y"):
        bot.send_message(message.chat.id, 'Нельзя ввести дату, которая уже прошла. Повторите снова')
        bot.register_next_step_handler(message, accept_time)
        return
    bot.send_message(message.chat.id, 'Введите время в формате:\n'
                                      'начало-конец\n'
                                      'Пример: 12:10-14:00\n'
                                      'Если какого-то времени нет, введите вместо него *')
    bot.register_next_step_handler(message, add_note)


def add_note(message):
    global now_family, now_note, now_user_id, now_date
    time = message.text.strip()
    time = time.replace('*', 'Null')
    time = time.split('-')
    if len(time) != 2:
        bot.send_message(message.chat.id, 'Данные введены не корректно, попробуйте снова')
        bot.register_next_step_handler(message, add_note)
        return
    elif compare_dates(time[0], time[1], "%H:%M"):
        bot.send_message(message.chat.id, 'Время начала не может быть позже время конца. Повторите снова')
        bot.register_next_step_handler(message, add_note)
        return
    # elif check_now_dates(time[0], "%H:%M") or check_now_dates(time[1], "%H:%M"):
    #     bot.send_message(message.chat.id, 'Нельзя ввести время, которая уже прошла. Повторите снова')
    #     bot.register_next_step_handler(message, add_note)
    #     return
    new_note(now_user_id, now_note, now_date[0], now_date[1], time[0], time[1], now_family)
    bot.send_message(message.chat.id, 'Вы успешно добавили событие')


@bot.message_handler(commands=['view_notes'])
def view_notes(message):
    global now_family
    if now_family == '':
        bot.send_message(message.chat.id, 'В данный момент семья не выбрана')
        return
    notes = view_info('list_notes', now_family)
    info = 'Список событий семьи:\n'
    for note in notes:
        info += f'{note}\n'
    bot.send_message(message.chat.id, info)


@bot.message_handler(commands=['view_family'])
def view_family(message):
    global now_family
    if now_family == '':
        bot.send_message(message.chat.id, 'В данный момент семья не выбрана')
        return
    persons = view_info('list_family', now_family)
    info = f'Список семьи {now_family}:\n'
    for person in persons:
        info += f'{person[1].capitalize()} {person[2].capitalize()} {person[3]}\n'
    bot.send_message(message.chat.id, info)


@bot.message_handler(commands=['now_family'])
def write_now_family(message):
    global now_family
    answer = f'Выбрана семья: {now_family}' if now_family != '' else 'В данный момент семья не выбрана'
    bot.send_message(message.chat.id, answer)


@bot.message_handler(commands=['test'])
def accept_teg_user(message):
    bot.send_message(message.chat.id, f'{message.from_user.id} {message.from_user.username}')


bot.infinity_polling()
