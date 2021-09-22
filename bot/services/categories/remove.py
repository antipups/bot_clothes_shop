from bot.services.categories.categories_search import choise_category
from bot.services.categories.menu import categories_menu
from bot.util import *
from bot.validators import Validator


@bot.message_handler(func=lambda message: message.text == Button.CategoryMenu.Remove and
                                          message.from_user.id in Constants.Telegram.Admins)
def write_remove_category(message: Message):
    chat_id, text, message_id = get_info_from_message(message=message)
    send_message(chat_id=chat_id,
                 text=Messages.Admin.Categories.EnterTitleRemoveCategory,
                 reply_markup=markups.categories(callback=Callbacks.Category.Remove),)


@bot.callback_query_handler(func=lambda message: callback_handler(message, Callbacks.Category.Remove))
def remove_category(message: Message):
    chat_id, text, message_id = get_info_from_message(message=message,
                                                      callback_str=Callbacks.Category.Remove)
    status = choise_category(message=message,
                             callback=Callbacks.Category.Remove)
    if status == -1:
        categories_menu(message=message)
    elif status == 1:
        db_util\
            .CategoryWork()\
            .remove_category(category_id=db_util
                             .SessionWork
                             .get(chat_id=chat_id,
                                  key='parent_id'))
        send_message(chat_id=chat_id,
                     text=Messages.Admin.Categories.SuccessRemoveCategory,
                     reply_markup=markups.category_menu())


# @bot.message_handler(func=lambda message: message.text == Button.CategoryMenu.Change and
#                      message.from_user.id in Constants.Telegram.Admins)
# def categories_menu(message: Message):
#     chat_id, text, message_id = get_info_from_message(message=message)
#     send_message(chat_id=chat_id,
#                  text=Messages.Admin.Categories.EnterTitleChangeCategory,
#                  reply_markup=markups.categories(callback=Callbacks.Category.Change),)
