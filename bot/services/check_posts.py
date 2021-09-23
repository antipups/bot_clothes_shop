import time

from telebot.types import InputMediaPhoto

from bot.services.categories.categories_search import choise_category
from bot.services.start import start
from bot.util import *


@logging()
def preview_post(chat_id: int):
    post_data: dict = db_util.SessionWork.get(chat_id=chat_id,
                                              key='post')
    category_breads = list(category.title for category in db_util.CategoryWork().get_all_parents(category_id=post_data['category_id'])[::-1])
    category_breads[-1] = '<u>' + category_breads[-1] + '</u>'
    category_breads = ' -> '.join(category_breads)
    caption = Messages.Posts.OutputPost.format(post_data['title'],
                                               post_data['description'],
                                               post_data['price'],
                                               category_breads,
                                               post_data['phone_number'],
                                               post_data['username'])
    photos = tuple(InputMediaPhoto(media=photo) for photo in post_data['photos'])
    photos[0].caption, photos[0].parse_mode = caption, 'html'
    bot.send_media_group(chat_id=chat_id,
                         media=photos)


@logging()
def send_post(chat_id: int, post_id: int, new: bool = False):
    post = db_util.PostWork.get_post(post_id=post_id)

    category_breads = list(category.title for category in db_util.CategoryWork().get_all_parents(category_id=post.category_id)[::-1])
    category_breads[-1] = '<u>' + category_breads[-1] + '</u>'
    category_breads = ' -> '.join(category_breads)

    caption = Messages.Posts.PostPublicated if new else ''
    caption += Messages.Posts.OutputPost.format(post.title,
                                                post.description,
                                                post.price,
                                                category_breads,
                                                post.phone_number,
                                                post.username)
    photos = tuple(InputMediaPhoto(media=photo.file_id) for photo in post.pictures)
    photos[0].caption, photos[0].parse_mode = caption, 'html'

    bot.send_media_group(chat_id=chat_id,
                         media=photos)


@bot.message_handler(func=lambda message: message.text == Button.StartMenuAdmin.Posts)
@logging()
def post_menu(message: Message):
    chat_id, text, message_id = get_info_from_message(message=message)
    send_message(chat_id=chat_id,
                 text=Messages.Posts.ChoisePosts,
                 reply_markup=markups.post_menu())


def output_posts(chat_id: int, category_id: Union[str, int] = None):
    for post in db_util.PostWork.get_posts(category_id=category_id):
        send_post(chat_id=chat_id,
                  post_id=post.id)
        time.sleep(.3)


@bot.message_handler(func=lambda message: message.text == Button.StartMenuUsual.CheckPosts)
@bot.message_handler(commands=Commands.All)
@logging()
def all_posts(message: Message):
    chat_id, text, message_id = get_info_from_message(message=message)
    output_posts(chat_id=chat_id)
    send_message(chat_id=chat_id,
                 text=Messages.Posts.ChoisePosts,
                 reply_markup=markups.post_menu())


@bot.message_handler(func=lambda message: message.text == Button.StartMenuUsual.CertainPosts)
@bot.message_handler(commands=Commands.Categories)
@logging()
def categories_posts(message: Message):
    chat_id, text, message_id = get_info_from_message(message=message)
    db_util.SessionWork.set(chat_id=chat_id,
                            key='parent_id',
                            value=None)
    send_message(chat_id=chat_id,
                 text=Messages.Posts.ChoisePostsCategory,
                 reply_markup=markups.categories(callback=Callbacks.Category.OutputPosts))


@bot.callback_query_handler(func=lambda message: callback_handler(message, Callbacks.Category.OutputPosts))
def set_change_category(message: Message):
    chat_id, text, message_id = get_info_from_message(message=message,
                                                      callback_str=Callbacks.Category.OutputPosts)
    status = choise_category(message=message,
                             callback=Callbacks.Category.OutputPosts)
    if status == -1:
        post_menu(message=message)
    elif status == 1:
        output_posts_by_category(chat_id=chat_id)


def output_posts_by_category(chat_id: int):
    category_id = db_util.SessionWork.get(chat_id=chat_id,
                                          key='parent_id')
    if posts := db_util.PostWork.get_posts(category_id=category_id):
        output_posts(chat_id=chat_id,
                     category_id=category_id)
        breadcrumbs = list(category.title for category in db_util.CategoryWork().get_all_parents(category_id=category_id)[::-1])
        breadcrumbs[-1] = f'<u>{breadcrumbs[-1]}</u>'
        text = Messages.Posts.AllCategoryPosts\
            .format(' -> '.join(breadcrumbs))

        offset = db_util.SessionWork.get(chat_id=chat_id,
                                         key='offset_posts')

        if len(posts):
            ...

        send_message(chat_id=chat_id,
                     text=text,
                     reply_markup=markups.post_menu())

    else:
        text = Messages.Posts.CategoryNotPosts
        send_message(chat_id=chat_id,
                     text=text,
                     reply_markup=markups.post_menu())
