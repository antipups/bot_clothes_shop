from bot.util import *


@bot.message_handler(func=lambda message: message.text == Button.StartMenuAdmin.Categories and
                                          message.from_user.id in Constants.Telegram.Admins)
def categories_menu(message: Message):
    chat_id, text, message_id = get_info_from_message(message=message)
    send_message(chat_id=chat_id,
                 text=Messages.Admin.Categories.ChoiseCategoryAction,
                 reply_markup=markups.category_menu())
