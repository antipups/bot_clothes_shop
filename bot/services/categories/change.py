from bot.services.categories.categories_search import choise_category
from bot.services.categories.menu import categories_menu
from bot.util import *
from bot.validators import Validator


@bot.message_handler(func=lambda message: message.text == Button.CategoryMenu.Change and
                                          message.from_user.id in Constants.Telegram.Admins)
def choise_change_category(message: Message):
    chat_id, text, message_id = get_info_from_message(message=message)
    send_message(chat_id=chat_id,
                 text=Messages.Admin.Categories.EnterTitleChangeCategory,
                 reply_markup=markups.categories(callback=Callbacks.Category.Change),)


@bot.callback_query_handler(func=lambda message: callback_handler(message, Callbacks.Category.Change))
def set_change_category(message: Message):
    chat_id, text, message_id = get_info_from_message(message=message,
                                                      callback_str=Callbacks.Category.Change)
    status = choise_category(message=message,
                             callback=Callbacks.Category.Change)
    if status == -1:
        categories_menu(message=message)
    elif status == 1:
        get_title_category(chat_id=chat_id)


def get_title_category(chat_id: int, text: str = Messages.Admin.Categories.EnterNewTitleChangeCategory):
    schedule_message(chat_id=chat_id,
                     text=text,
                     reply_markup=markups.back(),
                     method=rename_category)


def rename_category(message: Message):
    chat_id, text, message_id = get_info_from_message(message=message)

    if text == Button.Direction.Back:
        choise_change_category(message=message)

    else:
        if Validator.category_title(value=text):
            db_util.CategoryWork.change_category(category_id=db_util.SessionWork.get(chat_id=chat_id,
                                                                                     key='parent_id'),
                                                 new_title=text)
            send_message(chat_id=chat_id,
                         text=Messages.Admin.Categories.SuccessChangeCategory,
                         reply_markup=markups.category_menu())
        else:
            get_title_category(chat_id=chat_id,
                               text=Messages.Admin.Categories.EnterTitleWithoutErrors.format(db_util.Constants.LengthCategoryTitle))
