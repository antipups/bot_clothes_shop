import database.util as db_util
from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from database.config import Constants as db_constants
from bot.config import Button, Keyboard, Constants
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


def start_menu(chat_id: int) -> ReplyKeyboardMarkup:
    return _reply_markup(keyboard=Keyboard.StartMenuAdmin if db_util.is_admin(chat_id=chat_id) else Keyboard.StartMenuUsual)
