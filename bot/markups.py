from typing import Union

import database.util as db_util
from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from database.config import Constants as db_constants
from bot.config import Button, Keyboard, Constants, Callbacks
from copy import deepcopy


def _reply_markup(keyboard: list = [],
                  back_: bool = False,
                  continue_: bool = False,
                  one_time: bool = False,
                  main_menu_: bool = False) -> ReplyKeyboardMarkup:
    """
        Паттерн для DRY для replymarkup
    :param keyboard: нужная клавиатура
    :param back_: если нужно назад - истина
    :param continue_: если нужно продолжить - истина
    :param main_menu_: кнопка в главное меню
    :return:
    """
    markup = ReplyKeyboardMarkup(resize_keyboard=True,
                                 one_time_keyboard=one_time)

    if keyboard:
        for row in keyboard:
            button_row = [button_title for button_title in row]
            markup.add(*button_row)

    if continue_:
        markup.add(Button.Direction.Continue)

    if back_:
        markup.add(Button.Direction.Back)

    if main_menu_:
        markup.add(Button.Direction.MainMenu)

    return markup


def back() -> ReplyKeyboardMarkup:
    return _reply_markup(back_=True)


def start_menu(chat_id: int) -> ReplyKeyboardMarkup:
    return _reply_markup(keyboard=Keyboard.StartMenuAdmin if db_util.UsersWork.is_admin(chat_id=chat_id) else Keyboard.StartMenuUsual)


def category_menu() -> ReplyKeyboardMarkup:
    return _reply_markup(keyboard=Keyboard.CategoryMenu,
                         main_menu_=True)


def categories(callback: str, parent_id: Union[str, int] = 0):
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = []

    if parent_id == -1:  # при добавлении категории давать доступ к добавлению в главный список
        markup.add(InlineKeyboardButton(text='Главная категория',
                                        callback_data=callback.format(0)))
        parent_id = None

    categories_list: list[db_util.Categories] = db_util.CategoryWork.get_categories(parent_id=parent_id)
    for category in categories_list:
        buttons.append(InlineKeyboardButton(text=category.title,
                                            callback_data=callback.format(category.id)))

    markup.add(*buttons)
    markup.add(InlineKeyboardButton(text=Button.Direction.Back,
                                    callback_data=callback.format('back')))

    return markup
