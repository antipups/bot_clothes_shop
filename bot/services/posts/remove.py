from bot.util import *


@bot.callback_query_handler(func=lambda message: callback_handler(message, Callbacks.ChangePost) and
                                                 Button.Posts.Remove in message.data)
def remove_post(message: Message):
    chat_id, text, message_id = get_info_from_message(message=message,
                                                      callback_str=Callbacks.ChangePost)
    db_util.PostWork.remove_post(post_id=text.split('_')[-1])
    delete_message(chat_id=chat_id,
                   message_id=message_id)
