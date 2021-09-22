from general_config import logger


class Constants:
    class Telegram:
        Token = '889368628:AAGO10iS0nVkRlbvQre_OpgjDG2qlEbsK4s'

        Admins = (704369002,
                  )


class Commands:
    Start = ['start']


class Button:
    class Direction:
        Back = '🔙 Назад'
        NextPage = '▶️ Следующая страница'
        Continue = '➡️ Продолжить'
        MainMenu = '🗃 Главное меню'

    class StartMenuAdmin:
        NewPost = '🆕 Новое объявление'
        Categories = '🗂 Работа с категориями'
        NewAdmin = '🤴 Новый администратор'

    class StartMenuUsual:
        CheckPosts = 'Все объявления'
        CertainPosts = 'Определённая категория'

    class CategoryMenu:
        Add = '➕ Добавить категорию'
        Change = '✏️ Изменить категорию'
        Remove = '➖ Удалить категорию'

    class CategoryManipulation:
        Add = 'Добавить в данную категорию'
        Change = 'Изменить название данной категории'
        Remove = 'Удалить данную категорию'


class Keyboard:
    StartMenuAdmin = [[Button.StartMenuAdmin.NewPost, Button.StartMenuAdmin.Categories, Button.StartMenuAdmin.NewAdmin]]
    StartMenuUsual = [[Button.StartMenuUsual.CheckPosts, Button.StartMenuUsual.CertainPosts]]

    CategoryMenu = [[Button.CategoryMenu.Remove, Button.CategoryMenu.Change, Button.CategoryMenu.Add]]


class Callbacks:
    class Category:
        Remove = 'rmcat_{}'
        Change = 'cncat_{}'
        Add = 'mkcat_{}'


class Messages:
    StartMenu = '👋 Добро пожаловать!\n' \
                '☝️ Выберите что хотите посмотреть'

    class Admin:
        class Categories:
            ChoiseCategoryAction = '🤔 Что вы хотите сделать?'

            SelectedCategory = '🧭 Выбранная категория:<b>\n{}</b>'

            EnterTitleRemoveCategory = '✍️ Выберите категорию которую хотите <b>удалить</b>'
            SuccessRemoveCategory = '❌ Выбранная категория <b>удалена</b>, и все объявления которые были в ней тоже <b>удалены</b>'

            EnterTitleChangeCategory = '✍️ Выберите название категории которую хотите <b>переименовать</b>'
            EnterNewTitleChangeCategory = '✍️ Введите <b>новое</b> название данной категории'
            SuccessChangeCategory = '✅ Категория успешно <b>переименована</b>'

            EnterNewCategory = '✍️ Выберите <b>категорию</b> в <b>которую</b> хотели бы добавить <b>новую категорию</b>'
            EnterTitleNewCategory = '✍️ Введите название <b>новой</b> категории'
            EnterTitleWithoutErrors = '😖 Введите название <b>короче (максимум <u>{}</u> символов)</b>'
            SuccessAddCategory = '✅ Категория успешно <b>создана</b>'


