from bot.services.start import start
from bot.util import *


@bot.message_handler(func=lambda message: message.text == Button.StartMenuAdmin.NewAdmin and
                                          db_util.UsersWork.is_admin(message.from_user.id))
def new_admin(message: Message):
    chat_id, text, message_id = get_info_from_message(message=message)
    schedule_message(chat_id=chat_id,
                     text=Messages.Admin.SetAdmin.GetUserId,
                     reply_markup=markups.back(),
                     method=get_user_message)
    # db_util.UsersWork.is_registered(chat_id=chat_id)


def get_user_message(message: Message):
    chat_id, text, message_id = get_info_from_message(message=message)
    if text == Button.Direction.Back:
        start(message=message)

    elif message.forward_from:
        if db_util.UsersWork.is_registered(chat_id=message.forward_from.id):
            db_util.UsersWork.set_admin(chat_id=message.forward_from.id)
            send_message(chat_id=chat_id,
                         text=Messages.Admin.SetAdmin.SuccessAddAdmin,
                         reply_markup=markups.start_menu(chat_id=chat_id))
        else:
            send_message(chat_id=chat_id,
                         text=Messages.Admin.SetAdmin.ErrorNotFoundUser,
                         reply_markup=markups.start_menu(chat_id=chat_id))

    else:
        schedule_message(chat_id=chat_id,
                         text=Messages.Admin.SetAdmin.ErrorMessageType,
                         method=get_user_message)
