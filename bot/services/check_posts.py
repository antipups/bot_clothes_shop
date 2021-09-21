from bot.util import *


@bot.message_handler(func=lambda message: message.text == Button.StartMenuUsual.CheckPosts)
def all_posts(message: Message):
    chat_id, text, message_id = get_info_from_message(message=message)

