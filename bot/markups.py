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


def back(continue_: bool = False) -> ReplyKeyboardMarkup:
    return _reply_markup(back_=True,
                         continue_=continue_)


def start_menu(chat_id: int) -> ReplyKeyboardMarkup:
    return _reply_markup(keyboard=Keyboard.StartMenuAdmin if db_util.UsersWork.is_admin(chat_id=chat_id) else Keyboard.StartMenuUsual)


def category_menu() -> ReplyKeyboardMarkup:
    return _reply_markup(keyboard=Keyboard.CategoryMenu,
                         main_menu_=True)


def categories(callback: str, parent_id: Union[str, int] = None):
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = []

    if callback == Callbacks.Category.Add:
        markup.add(InlineKeyboardButton(text=Button.CategoryManipulation.Add,
                                        callback_data=callback.format(f'{parent_id}_1')))
    elif callback == Callbacks.Category.Remove and parent_id:
        markup.add(InlineKeyboardButton(text=Button.CategoryManipulation.Remove,
                                        callback_data=callback.format(f'{parent_id}_1')))
    elif callback == Callbacks.Category.Change and parent_id:
        markup.add(InlineKeyboardButton(text=Button.CategoryManipulation.Change,
                                        callback_data=callback.format(f'{parent_id}_1')))

    categories_list: list[db_util.Categories] = db_util.CategoryWork.get_categories(parent_id=parent_id)
    for category in categories_list:
        buttons.append(InlineKeyboardButton(text=category.title,
                                            callback_data=callback.format(category.id)))

    markup.add(*buttons)
    markup.add(InlineKeyboardButton(text=Button.Direction.Back,
                                    callback_data=callback.format('back')))

    return markup


def phone_number():
    return _reply_markup(keyboard=[[KeyboardButton(text=Button.CreatePost.PhoneNumber,
                                                   request_contact=True)]],
                         back_=True)


def username():
    return _reply_markup(keyboard=[[KeyboardButton(text=Button.CreatePost.Username)]],
                         back_=True)


def create_post():
    return _reply_markup(keyboard=Keyboard.CreatePost,
                         main_menu_=True)


def post_menu(next_: bool = False, prev_: bool = False):
    navigate_buttons = []
    if prev_:
        navigate_buttons.append(KeyboardButton(text=Button.Direction.PrevPage))
    if next_:
        navigate_buttons.append(KeyboardButton(text=Button.Direction.NextPage))

    keyboard = deepcopy(Keyboard.StartMenuUsual)

    if navigate_buttons:
        keyboard.insert(0, navigate_buttons)
        # keyboard.pop(1)

    return _reply_markup(keyboard=keyboard,
                         main_menu_=True)


def post_change_menu(post_id: int):
    markup = InlineKeyboardMarkup()
    markup.add(*(InlineKeyboardButton(text=button,
                                      callback_data=Callbacks.ChangePost.format(f'{button}_{post_id}')) for row in Keyboard.PostMenu for button in row))
    return markup


def change_post_choise(post_id: str):
    markup = InlineKeyboardMarkup()
    markup.add(*(InlineKeyboardButton(text=button,
                                      callback_data=Callbacks.ChangeInlinePost.format(f'{button}_{post_id}')) for row in
                 Keyboard.ChangePost for button in row))
    return markup
