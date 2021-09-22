from bot.util import *


def choise_category(message: CallbackQuery, callback: str):
    """
        Выбор категорий, возврат -1 - если это шаг назад, 1 - если это шаг вперед
    :param message:
    :param callback:
    :return:
    """
    chat_id, text, message_id = get_info_from_message(message=message,
                                                      callback_str=callback)
    parent_id = db_util.SessionWork.get(chat_id=chat_id,
                                        key='parent_id')

    if callback == Callbacks.Category.Add:
        category_tree_text = Messages.Admin.Categories.EnterNewCategory
    elif callback == Callbacks.Category.Remove:
        category_tree_text = Messages.Admin.Categories.EnterTitleRemoveCategory
    elif callback == Callbacks.Category.Change:
        category_tree_text = Messages.Admin.Categories.EnterTitleChangeCategory

    if text == 'back' and not parent_id:
        return -1

    elif text == 'back':
        text = db_util.CategoryWork.get_category(category_id=parent_id).parent_id

    if isinstance(text, str) and '_' in text:
        # если выбрано добавить сюда*
        db_util.SessionWork.set(chat_id=chat_id,
                                key='parent_id',
                                value=text.split('_')[0])
    else:
        db_util.SessionWork.set(chat_id=chat_id,
                                key='parent_id',
                                value=text)

    if db_util.CategoryWork.get_categories(parent_id=text):
        bot.edit_message_text(chat_id=chat_id,
                              message_id=message_id,
                              text=category_tree(current_category_id=text,
                                                 text=category_tree_text),
                              reply_markup=markups.categories(parent_id=text,
                                                              callback=callback))
    else:
        bot.edit_message_text(chat_id=chat_id,
                              message_id=message_id,
                              text=category_tree(current_category_id=db_util.SessionWork.get(chat_id=chat_id,
                                                                                             key='parent_id'),
                                                 text=category_tree_text,
                                                 last_selected=True),
                              reply_markup=None)
        return 1
