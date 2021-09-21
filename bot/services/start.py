from bot.util import *


@bot.message_handler(commands=Commands.START)
def start(message: Message):
    chat_id, text, message_id = get_info_from_message(message=message)
    if not db_util.is_registered(chat_id=chat_id):
        db_util.new_user(chat_id=chat_id,
                         username=message.from_user.username)
    send_message(chat_id=chat_id,
                 text=Messages.StartMenu,
                 reply_markup=markups.start_menu(chat_id=chat_id))
