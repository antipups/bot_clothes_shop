from typing import Union
from telebot import TeleBot
from telebot.types import BotCommand, CallbackQuery, Message, BotCommandScope
from bot.config import *
import database.util as db_util
from bot import markups


bot = TeleBot(token=Constants.Telegram.Token,
              parse_mode='html')


# bot.set_my_commands([BotCommand(command, description) for command, description in COMMAND_DESCRIPTIONS.items()],
#                     language_code='ru')
# bot.set_my_commands([BotCommand(command, description) for command, description in COMMAND_DESCRIPTIONS_ON_UZB.items()],
#                     language_code='uz')


def start_bot():
    logger.info('Bot Started')
    bot.remove_webhook()
    bot.infinity_polling()


def send_message(chat_id: int, text: str, reply_markup=None, disable_web_page_preview: bool = False):
    try:
        bot.send_message(chat_id=chat_id,
                         text=text,
                         reply_markup=reply_markup,
                         disable_web_page_preview=disable_web_page_preview)
    except Exception as e:
        logger.error(f'Error in send_message cause - {e}, chat_id - {chat_id}')


def get_info_from_message(message: Union[Message, CallbackQuery], callback_str: str = '') -> tuple[int, str, int]:
    """
        Метод для получения данных с сообщения будь-то колбека или обычного
    :param callback_str: коллбек начало которое нужно обрезать
    :param message: необходимое сообщение
    :return: айди, текст, айди сообщения
    """
    if isinstance(message, Message):
        if message.content_type != 'text':
            return message.from_user.id, message.caption, message.message_id
        else:
            return message.from_user.id, message.text, message.message_id
    else:
        return message.from_user.id, message.data[len(callback_str) - 2:], message.message.message_id


def schedule_message(chat_id: int, text: str, method, reply_markup=None):
    """
        Метод для регистрации следующего шага, чтоб писать меньше строк
    :param reply_markup:
    :param chat_id: кому отправлять
    :param text:    текст сообщения
    :param method:  нужный метод
    :param markup:  нужная клавиатура
    :return:
    """
    try:
        msg = bot.send_message(chat_id=chat_id,
                               text=text,
                               reply_markup=reply_markup,
                               parse_mode='html')
    except Exception as e:      # если бота заблокировали
        logger.error(f'Не удалось отправить сообщение с регистрацией шага из-за ошибки \n {e}')
    else:
        bot.register_next_step_handler(msg, method)
        return msg


def delete_message(chat_id: int,
                   message_id: int):
    """
        Удаление сообщения из канала с отловом эксепшина
    :param chat_id:
    :param message_id:
    :return:
    """
    try:
        bot.delete_message(chat_id=chat_id,
                           message_id=message_id)
    except Exception as e:
        logger.error(f'Не удалось удалить сообщение из-за ошибки \n {e}')
