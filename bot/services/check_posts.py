import time

from telebot.types import InputMediaPhoto

from bot.services.categories.categories_search import choise_category
from bot.services.start import start
from bot.util import *


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
    try:
        bot.send_media_group(chat_id=chat_id,
                             media=photos)
    except Exception as e:
        logger.exception('Error in output PREVIEW')
        send_message(chat_id=chat_id,
                     text=caption)


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

    try:
        if db_util.UsersWork.is_admin(chat_id=chat_id):
            bot.send_photo(chat_id=chat_id,
                           photo=photos[0].media,
                           caption=photos[0].caption,
                           reply_markup=markups.post_change_menu(post_id=post_id))
        else:
            bot.send_media_group(chat_id=chat_id,
                                 media=photos)
    except Exception as e:
        logger.exception('Error in output POSTS')
        send_message(chat_id=chat_id,
                     text=caption)


@bot.message_handler(func=lambda message: message.text == Button.StartMenuAdmin.Posts)
def post_menu(message: Message):
    chat_id, text, message_id = get_info_from_message(message=message)
    send_message(chat_id=chat_id,
                 text=Messages.Posts.ChoisePosts,
                 reply_markup=markups.post_menu())


def output_posts(chat_id: int,
                 category_id: Union[str, int] = None):
    offset = db_util.SessionWork.get(chat_id=chat_id,
                                     key='offset')
    posts_offset = offset * db_util.Constants.OutputAmountPostsLimit
    for post in db_util.PostWork.get_posts(category_id=category_id)[posts_offset:posts_offset + db_util.Constants.OutputAmountPostsLimit:][::-1]:
        send_post(chat_id=chat_id,
                  post_id=post.id)
        time.sleep(.3)


@bot.message_handler(func=lambda message: message.text == Button.StartMenuUsual.CheckPosts)
@bot.message_handler(commands=Commands.All)
def all_posts(message: Message):
    chat_id, text, message_id = get_info_from_message(message=message)
    db_util.SessionWork.set(chat_id=chat_id,
                            key='parent_id',
                            value=None)
    db_util.SessionWork.set(chat_id=chat_id,
                            key='offset',
                            value=0)
    output_posts_by_category(chat_id=chat_id)


@bot.message_handler(func=lambda message: message.text == Button.StartMenuUsual.CertainPosts)
@bot.message_handler(commands=Commands.Categories)
def categories_posts(message: Message):
    print('sex')
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
        db_util.SessionWork.set(chat_id=chat_id,
                                key='offset',
                                value=0)


def output_posts_by_category(message: Message = None,
                             chat_id: int = 0):
    """
        Вывод объявлений по категориям
    :param message: если кликнули на какую-то кнопку после вывода первой страницы категорий
    :param chat_id: вывод первой страницы категории по данному параметру
    :param admin: если админ к категориям клеим ещё вывод клавиатуры
    :return:
    """
    if message:
        chat_id, text, message_id = get_info_from_message(message=message)

    if message and text == Button.Direction.MainMenu:
        start(message=message)
        return

    elif message and text == Button.StartMenuUsual.CheckPosts:
        all_posts(message=message)
        return

    elif message and text == Button.StartMenuUsual.CertainPosts:
        categories_posts(message=message)
        return

    if message and text == Button.Direction.NextPage:
        db_util.SessionWork.set(chat_id=chat_id,
                                key='offset',
                                value=db_util.SessionWork.get(chat_id=chat_id,
                                                              key='offset') + 1)
    if message and text == Button.Direction.PrevPage:
        db_util.SessionWork.set(chat_id=chat_id,
                                key='offset',
                                value=db_util.SessionWork.get(chat_id=chat_id,
                                                              key='offset') - 1)

    get_step_hendler_for_search(chat_id=chat_id)


def get_step_hendler_for_search(chat_id: int, all_post_output: bool = True):
    """
        Генерация просмотра постов для пользователя и админа с клавиатурой
    :param chat_id: кому выводим
    :param all_post_output: все посты или нет (если редактирование - не выводим, только вешаем обработчик)
    :return:
    """
    category_id = db_util.SessionWork.get(chat_id=chat_id,
                                          key='parent_id')
    if posts := db_util.PostWork.get_posts(category_id=category_id):
        if category_id:
            breadcrumbs = list(
                category.title for category in db_util.CategoryWork().get_all_parents(category_id=category_id)[::-1])
            breadcrumbs[-1] = f'<u>{breadcrumbs[-1]}</u>'
            text = Messages.Posts.CategoryPosts \
                .format(' -> '.join(breadcrumbs))
        else:
            text = Messages.Posts.AllPosts

        prev_, next_ = False, False
        amount_posts = len(posts)

        if amount_posts > db_util.Constants.OutputAmountPostsLimit:
            offset = db_util.SessionWork.get(chat_id=chat_id,
                                             key='offset')
            if offset > 0:
                prev_ = True
            if amount_posts > offset * db_util.Constants.OutputAmountPostsLimit + db_util.Constants.OutputAmountPostsLimit:
                next_ = True

        if all_post_output:
            output_posts(chat_id=chat_id,
                         category_id=category_id)

        schedule_message(chat_id=chat_id,
                         text=text,
                         reply_markup=markups.post_menu(next_=next_,
                                                        prev_=prev_),
                         method=output_posts_by_category)

    else:
        text = Messages.Posts.CategoryNotPosts
        send_message(chat_id=chat_id,
                     text=text,
                     reply_markup=markups.post_menu())
