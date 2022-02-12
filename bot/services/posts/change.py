from bot.services.check_posts import send_post, get_step_hendler_for_search
from bot.util import *
from bot.validators import Validator


@bot.callback_query_handler(func=lambda message: callback_handler(message, Callbacks.ChangePost) and
                                                 Button.Posts.Change in message.data)
def change_post(message: CallbackQuery):
    chat_id, text, message_id = get_info_from_message(message=message,
                                                      callback_str=Callbacks.ChangePost)
    bot.edit_message_caption(chat_id=chat_id,
                             message_id=message_id,
                             caption=message.message.caption + '\n\n' + Messages.Posts.ChangeChoise,
                             reply_markup=markups.change_post_choise(post_id=text.split('_')[-1]))


@bot.callback_query_handler(func=lambda message: callback_handler(message, Callbacks.ChangeInlinePost) and
                                                 Button.Posts.Description in message.data)
def change_description(message: CallbackQuery):
    chat_id, text, message_id = get_info_from_message(message=message,
                                                      callback_str=Callbacks.ChangeInlinePost)
    bot.clear_step_handler_by_chat_id(chat_id=chat_id)
    db_util.SessionWork.set(chat_id=chat_id,
                            key='post_id',
                            value=text.split('_')[-1])
    delete_message(chat_id=chat_id,
                   message_id=message_id)
    get_description(chat_id=chat_id)


def get_description(chat_id: int, text: str = Messages.Admin.CreatePost.EnterDescription):
    schedule_message(chat_id=chat_id,
                     text=text.format(db_util.Constants.LengthPostDescription),
                     reply_markup=markups.back(),
                     method=set_description)


def set_description(message: Message):
    chat_id, text, message_id = get_info_from_message(message=message)

    post_id = db_util.SessionWork.get(chat_id=chat_id,
                                      key='post_id')

    if text == Button.Direction.Back:
        send_post(chat_id=chat_id,
                  post_id=post_id)
        get_step_hendler_for_search(chat_id=chat_id,
                                    all_post_output=False)

    elif Validator.post_description(value=text):
        db_util.PostWork.set_new_description(post_id=post_id,
                                             description=text)
        send_post(chat_id=chat_id,
                  post_id=post_id)
        get_step_hendler_for_search(chat_id=chat_id,
                                    all_post_output=False)

    else:
        get_description(chat_id=chat_id,
                        text=Messages.Admin.CreatePost.ErrorDescriptionLength)


@bot.callback_query_handler(func=lambda message: callback_handler(message, Callbacks.ChangeInlinePost) and
                                                 Button.Posts.Price in message.data)
def change_price(message: CallbackQuery):
    chat_id, text, message_id = get_info_from_message(message=message,
                                                      callback_str=Callbacks.ChangeInlinePost)
    bot.clear_step_handler_by_chat_id(chat_id=chat_id)
    db_util.SessionWork.set(chat_id=chat_id,
                            key='post_id',
                            value=text.split('_')[-1])
    delete_message(chat_id=chat_id,
                   message_id=message_id)
    get_price(chat_id=chat_id)


def get_price(chat_id: int, text: str = Messages.Admin.CreatePost.EnterPrice):
    schedule_message(chat_id=chat_id,
                     text=text.format(db_util.Constants.LengthPostPrice),
                     reply_markup=markups.back(),
                     method=set_price)


def set_price(message: Message):
    chat_id, text, message_id = get_info_from_message(message=message)

    post_id = db_util.SessionWork.get(chat_id=chat_id,
                                      key='post_id')

    if text == Button.Direction.Back:
        send_post(chat_id=chat_id,
                  post_id=post_id)
        get_step_hendler_for_search(chat_id=chat_id,
                                    all_post_output=False)

    elif Validator.post_price(value=text):
        db_util.PostWork.set_new_price(post_id=post_id,
                                       price=text)
        send_post(chat_id=chat_id,
                  post_id=post_id)
        get_step_hendler_for_search(chat_id=chat_id,
                                    all_post_output=False)

    else:
        get_price(chat_id=chat_id,
                  text=Messages.Admin.CreatePost.ErrorPriceLength)
