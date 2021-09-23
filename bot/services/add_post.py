import time

from bot.services.categories.categories_search import choise_category
from bot.services.check_posts import preview_post, send_post
from bot.services.start import start
from bot.util import *
from bot.validators import Validator


@bot.message_handler(func=lambda message: message.text == Button.StartMenuAdmin.NewPost and
                                          db_util.UsersWork.is_admin(message.from_user.id))
@logging()
def start_create_post(message: Message):
    chat_id, text, message_id = get_info_from_message(message=message)
    get_post_title(chat_id=chat_id)


def get_post_title(chat_id: int,
                   text: str = Messages.Admin.CreatePost.EnterTitle):
    schedule_message(chat_id=chat_id,
                     text=text.format(db_util.Constants.LengthPostTitle),
                     reply_markup=markups.back(),
                     method=set_title)


@logging()
def set_title(message: Message):
    chat_id, text, message_id = get_info_from_message(message=message)

    if text == Button.Direction.Back:
        start(message=message)

    elif Validator.post_title(value=text):
        db_util.SessionWork.set(chat_id=chat_id,
                                key='post___title',
                                value=text)
        get_post_description(chat_id=chat_id)

    else:
        get_post_title(chat_id=chat_id,
                       text=Messages.Admin.CreatePost.ErrorTitleLength)


def get_post_description(chat_id: int,
                         text: str = Messages.Admin.CreatePost.EnterDescription):
    schedule_message(chat_id=chat_id,
                     text=text.format(db_util.Constants.LengthPostDescription),
                     reply_markup=markups.back(),
                     method=set_description)


@logging()
def set_description(message: Message):
    chat_id, text, message_id = get_info_from_message(message=message)

    if text == Button.Direction.Back:
        get_post_title(chat_id=chat_id)

    elif Validator.post_description(value=text):
        db_util.SessionWork.set(chat_id=chat_id,
                                key='post___description',
                                value=text)
        get_post_price(chat_id=chat_id)

    else:
        get_post_description(chat_id=chat_id,
                             text=Messages.Admin.CreatePost.ErrorDescriptionLength)


def get_post_price(chat_id: int,
                   text: str = Messages.Admin.CreatePost.EnterPrice):
    schedule_message(chat_id=chat_id,
                     text=text.format(db_util.Constants.LengthPostPrice),
                     reply_markup=markups.back(),
                     method=set_price)


@logging()
def set_price(message: Message):
    chat_id, text, message_id = get_info_from_message(message=message)

    if text == Button.Direction.Back:
        get_post_description(chat_id=chat_id)

    elif Validator.post_price(value=text):
        db_util.SessionWork.set(chat_id=chat_id,
                                key='post___price',
                                value=text)
        get_category(chat_id=chat_id)

    else:
        get_post_price(chat_id=chat_id,
                       text=Messages.Admin.CreatePost.ErrorDescriptionLength)


def get_category(chat_id: int):
    send_message(chat_id=chat_id,
                 text=Messages.Admin.CreatePost.EnterCategory,
                 reply_markup=markups.categories(callback=Callbacks.Category.CreatePost))


@bot.callback_query_handler(func=lambda message: callback_handler(message, Callbacks.Category.CreatePost))
def set_category(message: Message):
    chat_id, text, message_id = get_info_from_message(message=message,
                                                      callback_str=Callbacks.Category.CreatePost)
    status = choise_category(message=message,
                             callback=Callbacks.Category.CreatePost)
    if status == -1:
        delete_message(chat_id=chat_id,
                       message_id=message_id)
        get_post_price(chat_id=chat_id)

    elif status == 1:
        category_id = db_util.SessionWork.get(chat_id=chat_id,
                                              key='parent_id')
        db_util.SessionWork.set(chat_id=chat_id,
                                key='post___category_id',
                                value=category_id)
        db_util.SessionWork.set(chat_id=chat_id,
                                key='post___photos',
                                value=[])
        get_picture(chat_id=chat_id)


def get_picture(chat_id: int,
                text: str = Messages.Admin.CreatePost.EnterPicture.format(1),
                continue_: bool = False):
    schedule_message(chat_id=chat_id,
                     text=text,
                     reply_markup=markups.back(continue_=continue_),
                     method=set_picture)


@logging()
def set_picture(message: Message):
    chat_id, text, message_id = get_info_from_message(message=message)

    if text == Button.Direction.Back:
        get_category(chat_id=chat_id)

    elif message.content_type == 'photo':

        amount_photos = db_util.SessionWork.add_photo(chat_id=chat_id,
                                                      file_id=message.photo[-1].file_id)
        get_picture(chat_id=chat_id,
                    text=Messages.Admin.CreatePost.EnterPicture.format(amount_photos + 1) +
                         '\n☝️ Для продолжения подачи объявления, нажмите <b>{}</b>'.format(Button.Direction.Continue),
                    continue_=True)

    elif text == Button.Direction.Continue and db_util.SessionWork.get(chat_id=chat_id,
                                                                       key='post')['photos']:
        get_phone_number(chat_id=chat_id)

    else:
        get_picture(chat_id=chat_id,
                    text=Messages.Admin.CreatePost.ErrorEnterPicture)


def get_phone_number(chat_id: int,
                     text: str = Messages.Admin.CreatePost.EnterPhone):
    schedule_message(chat_id=chat_id,
                     text=text.format(db_util.Constants.LengthPostPhone),
                     reply_markup=markups.phone_number(),
                     method=set_phone_number)


@logging()
def set_phone_number(message: Message):
    chat_id, text, message_id = get_info_from_message(message=message)

    if text == Button.Direction.Back:
        get_picture(chat_id=chat_id)

    elif message.content_type == 'contact' or Validator.post_phone_number(value=text):

        if message.content_type == 'contact':
            phone_number = message.contact.phone_number
        else:
            phone_number = text

        db_util.SessionWork.set(chat_id=chat_id,
                                key='post___phone_number',
                                value=phone_number)
        get_username(chat_id=chat_id,
                     text=Messages.Admin.CreatePost.EnterUsername.format(message.from_user.username))

    else:
        get_phone_number(chat_id=chat_id,
                         text=Messages.Admin.CreatePost.ErrorEnterPhone)


def get_username(chat_id: int,
                 text: str):
    schedule_message(chat_id=chat_id,
                     text=text,
                     reply_markup=markups.username(),
                     method=set_username)


@logging()
def set_username(message: Message):
    chat_id, text, message_id = get_info_from_message(message=message)

    if text == Button.Direction.Back:
        get_phone_number(chat_id=chat_id)

    elif text == Button.CreatePost.Username or Validator.post_username(value=text):

        if text == Button.CreatePost.Username:
            username = message.from_user.username
        else:
            username = text.replace('@', '')

        db_util.SessionWork.set(chat_id=chat_id,
                                key='post___username',
                                value=username)
        get_preview_post(chat_id=chat_id)

    else:
        get_username(chat_id=chat_id,
                     text=Messages.Admin.CreatePost.ErrorEnterUsername
                     .format(db_util.Constants.LengthPostUsername))


@logging()
def get_preview_post(chat_id: int):
    preview_post(chat_id=chat_id)
    schedule_message(chat_id=chat_id,
                     text=Messages.Admin.CreatePost.SendPost,
                     reply_markup=markups.create_post(),
                     method=publicate)


@logging()
def publicate(message: Message):
    chat_id, text, message_id = get_info_from_message(message=message)

    if text == Button.CreatePost.Reset:
        start_create_post(message=message)

    elif text == Button.CreatePost.SendPost:
        post_id = db_util.PostWork.new_post(post_data=db_util.SessionWork.get(chat_id=chat_id,
                                                                              key='post'))
        send_message(chat_id=chat_id,
                     text=Messages.Admin.CreatePost.SuccessSendPost,
                     reply_markup=markups.start_menu(chat_id=chat_id))
        for user in db_util.UsersWork.get_all_users():
            send_post(chat_id=user.id,
                      post_id=post_id,
                      new=True)
            time.sleep(.3)

    else:
        start(message=message)


