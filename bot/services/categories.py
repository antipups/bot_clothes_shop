from bot.services.categories_search import choise_category
from bot.util import *
from bot.services import start
from bot.validators import Validator


@bot.message_handler(func=lambda message: message.text == Button.StartMenuAdmin.Categories and
                     message.from_user.id in Constants.Telegram.Admins)
def categories_menu(message: Message):
    chat_id, text, message_id = get_info_from_message(message=message)
    send_message(chat_id=chat_id,
                 text=Messages.Admin.Categories.ChoiseCategoryAction,
                 reply_markup=markups.category_menu())


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
    if text == 'back':
        start.start(message=message)

    # else:
    #     schedule_message(chat_id=chat_id,
    #                      text=Messages.Admin.EnterTitleRemoveCategory,
    #                      reply_markup=markups.back(),
    #                      method=remove_category)


# @bot.message_handler(func=lambda message: message.text == Button.CategoryMenu.Change and
#                      message.from_user.id in Constants.Telegram.Admins)
# def categories_menu(message: Message):
#     chat_id, text, message_id = get_info_from_message(message=message)
#     send_message(chat_id=chat_id,
#                  text=Messages.Admin.Categories.EnterTitleChangeCategory,
#                  reply_markup=markups.categories(callback=Callbacks.Category.Change),)


@bot.message_handler(func=lambda message: message.text == Button.CategoryMenu.Add and
                     message.from_user.id in Constants.Telegram.Admins)
def choise_category_to_add(message: Message):
    chat_id, text, message_id = get_info_from_message(message=message)
    db_util.SessionWork.set(chat_id=chat_id,
                            key='parent_id',
                            value=None)
    send_message(chat_id=chat_id,
                 text=Messages.Admin.Categories.EnterNewCategory,
                 reply_markup=markups.categories(callback=Callbacks.Category.Add))


@bot.callback_query_handler(func=lambda message: callback_handler(message, Callbacks.Category.Add))
def write_new_category(message: CallbackQuery):
    chat_id, text, message_id = get_info_from_message(message=message)
    status = choise_category(message=message,
                             callback=Callbacks.Category.Add)
    if status == -1:
        categories_menu(message=message)
    elif status == 1:
        get_title_category(chat_id=chat_id)


def get_title_category(chat_id: int, text: str = Messages.Admin.Categories.EnterTitleNewCategory):
    schedule_message(chat_id=chat_id,
                     text=text,
                     reply_markup=markups.back(),
                     method=new_category)


def new_category(message: Message):
    chat_id, text, message_id = get_info_from_message(message=message)

    if text == Button.Direction.Back:
        choise_category_to_add(message=message)

    else:
        if Validator.category_title(value=text):
            db_util.CategoryWork.new_category(parent_id=db_util.SessionWork.get(chat_id=chat_id,
                                                                                key='parent_id'),
                                              title=text)
            send_message(chat_id=chat_id,
                         text=Messages.Admin.Categories.SuccessAddCategory,
                         reply_markup=markups.category_menu())
        else:
            get_title_category(chat_id=chat_id,
                               text=Messages.Admin.Categories.EnterTitleWithoutErrors.format(db_util.Constants.LengthCategoryTitle))
