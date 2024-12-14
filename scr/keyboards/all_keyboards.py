from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def kb_choice_family(families):
    kb_list = []
    for item in range(1, len(families), 2):
        kb_list.append([KeyboardButton(text=families[item - 1]), KeyboardButton(text=families[item])])
    if len(families) % 2 != 0:
        kb_list.append([KeyboardButton(text=families[-1])])
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True)
    return keyboard
