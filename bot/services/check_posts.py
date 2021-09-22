from telebot.types import InputMediaPhoto

from bot.util import *


def preview_post(chat_id: int):
    post_data: dict = db_util.SessionWork.get(chat_id=chat_id,
                                              key='post')
    category_breads = list(category.title for category in db_util.CategoryWork().get_all_parents(category_id=post_data['category_id'])[::-1])
    category_breads[-1] = '<u>' + category_breads[-1] + '</u>'
    category_breads = ' -> '.join(category_breads)
    caption = Messages.OutputPost.format(post_data['title'],
                                         post_data['description'],
                                         post_data['price'],
                                         category_breads,
                                         post_data['phone_number'],
                                         post_data['username'])
    photos = tuple(InputMediaPhoto(media=photo) for photo in post_data['photos'])
    photos[0].caption, photos[0].parse_mode = caption, 'html'
    bot.send_media_group(chat_id=chat_id,
                         media=photos)


def send_post(chat_id: int, post_id: int, new: bool = False):
    post = db_util.PostWork.get_post(post_id=post_id)

    category_breads = list(category.title for category in db_util.CategoryWork().get_all_parents(category_id=post.category_id)[::-1])
    category_breads[-1] = '<u>' + category_breads[-1] + '</u>'
    category_breads = ' -> '.join(category_breads)

    caption = Messages.PostPublicated if new else ''
    caption += Messages.OutputPost.format(post.title,
                                          post.description,
                                          post.price,
                                          category_breads,
                                          post.phone_number,
                                          post.username)
    photos = tuple(InputMediaPhoto(media=photo.file_id) for photo in post.pictures)
    photos[0].caption, photos[0].parse_mode = caption, 'html'

    bot.send_media_group(chat_id=chat_id,
                         media=photos)


@bot.message_handler(func=lambda message: message.text == Button.StartMenuUsual.CheckPosts)
def all_posts(message: Message):
    chat_id, text, message_id = get_info_from_message(message=message)

