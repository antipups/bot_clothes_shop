from bot.util import *


@bot.message_handler(func=lambda message: message.text == Button.Direction.MainMenu)
@bot.message_handler(commands=Commands.Start)
def start(message: Message):
    chat_id, text, message_id = get_info_from_message(message=message)

    if not db_util.UsersWork.is_registered(chat_id=chat_id):
        db_util.UsersWork.new_user(chat_id=chat_id,
                                   username=message.from_user.username)

    send_message(chat_id=chat_id,
                 text=Messages.StartMenu,
                 reply_markup=markups.start_menu(chat_id=chat_id))
