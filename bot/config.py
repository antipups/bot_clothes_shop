from general_config import *


class Constants:
    class Telegram:
        Token = '889368628:AAGO10iS0nVkRlbvQre_OpgjDG2qlEbsK4s'

        Admins = (704369002,
                  )


class Commands:
    Start = ['start']
    All = ['all']           # вывод всех постов
    Categories = ['cats']   # вывод постов по категориям


class CommandsDescription(Commands):
    def __init__(self):
        super(CommandsDescription, self).__init__()

    def get_commands(self):
        return ((super().Start[0], 'Стартовое меню'),
                (super().All[0], 'Показать все объявления'),
                (super().Categories[0], 'Показать объявления по категориям'))


class Button:
    class Direction:
        Back = '🔙 Назад'
        NextPage = '▶️ Следующая страница'
        PrevPage = '◀️ Предыдущая страница'
        Continue = '➡️ Продолжить'
        MainMenu = '🗃 Главное меню'

    class StartMenuAdmin:
        NewPost = '🆕 Новое объявление'
        Categories = '🗂 Работа с категориями'
        NewAdmin = '🤴 Новый администратор'
        Posts = '📮 Посмотреть объявления'

    class StartMenuUsual:
        CheckPosts = '📚 Все объявления'
        CertainPosts = '📗 Определённая категория'

    class CategoryMenu:
        Add = '➕ Добавить категорию'
        Change = '✏️ Изменить категорию'
        Remove = '➖ Удалить категорию'

    class CategoryManipulation:
        Add = '➕ Добавить в данную категорию'
        Change = '✍️ Изменить название данной категории'
        Remove = '➖ Удалить данную категорию'

    class CreatePost:
        PhoneNumber = '📲 Предоставить текущий номер телефона'
        Username = '👤 Предоставить текущее имя пользователя'

        SendPost = '📮 Опубликовать'
        Reset = '🔄 Создать объявление заново'


class Keyboard:
    StartMenuAdmin = [[Button.StartMenuAdmin.NewPost, Button.StartMenuAdmin.Categories, Button.StartMenuAdmin.NewAdmin],
                      [Button.StartMenuAdmin.Posts]]
    StartMenuUsual = [[Button.StartMenuUsual.CheckPosts, Button.StartMenuUsual.CertainPosts]]

    CategoryMenu = [[Button.CategoryMenu.Remove, Button.CategoryMenu.Change, Button.CategoryMenu.Add]]

    CreatePost = [[Button.CreatePost.Reset, Button.CreatePost.SendPost]]


class Callbacks:
    class Category:
        Remove = 'rmcat_{}'
        Change = 'cncat_{}'
        Add = 'mkcat_{}'

        CreatePost = 'mkpost_{}'

        OutputPosts = 'printposts_{}'


class Messages:
    StartMenu = '👋 Добро пожаловать!\n' \
                '☝️ Выберите что хотите посмотреть'

    class Posts:
        OutputPost = '✏️ Название: <b>{}</b>\n' \
                     '📝 Описание: <b>{}</b>\n' \
                     '💰 Цена: <b>{}</b>\n' \
                     '🗂 Категория: <b>{}</b>\n\n' \
                     '📱 Номер телефона: <code>{}</code>\n(клик по номеру для копирования)\n' \
                     '👤 Имя пользователя: @{}'
        # PostPublicated = '❕❕❕ Доступен новый товар ❕❕❕\n\n{}'
        PostPublicated = '👕👖🥾 <b>Доступен новый товар</b> 💄👗👠\n\n'

        ChoisePosts = '☝️ Выберите какие <b>объявления</b> вы хотите посмотреть'

        ChoisePostsCategory = '☝️ Выберите интересующую <b>вас</b> категорию'
        AllCategoryPosts = '📥 Все объявления в категории <b>"{}"</b> выведены выше'
        CategoryNotPosts = '😖 В данной категории на данный момент <b>нет объявлений</b>'

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

        class SetAdmin:
            GetUserId = '🏹 <b>Перешлите сообщение</b> от человека, <b>которого</b> хотите добавить в <b>администраторы</b>'
            SuccessAddAdmin = '🤴 Администратор <b>успешно</b> назначен'

            ErrorMessageType = '😖 Пожалуйста, <b>перешлите</b> сообщение человека которого хотите добавить в администраторы'
            ErrorNotFoundUser = '😖 Пользователь <b>не найден</b> в системе.\n' \
                                'Он должен вначале активировать бота,\n' \
                                'после данного действия вы сможете добавить его в систему'

        class CreatePost:
            EnterTitle = '✏️ Введите <b>название</b> объявления (макс. {} символа)'
            ErrorTitleLength = '😖 Введённое название <b>превышает</b> допустимое количество символов <b>(макс. {} символа)</b>'

            EnterDescription = '📝 Введите <b>описание</b> объявления (макс. {} символа)'
            ErrorDescriptionLength = '😖 Введённое описание <b>превышает</b> допустимое количество символов <b>(макс. {} символа)</b>'

            EnterPrice = '💰 Введите <b>цену</b> товара (макс. {} символов)'
            ErrorPriceLength = '😖 Введённая цена <b>превышает</b> допустимое количество символов <b>(макс. {} символа)</b>'

            EnterCategory = '🗂 Выберите <b>категорию</b> товара'

            EnterPicture = '📸 Пришлите {}-ую <b>фотографию</b>'
            ErrorEnterPicture = '😖 Пришлите <b>фотографию</b>'

            EnterPhone = '📱 Введите <b>номер телефона</b> (или можете использовать текущий)'
            ErrorEnterPhone = '😖 Введённый номер телефона <b>превышает</b> допустимое количество символов <b>(макс. {} символов)</b>'

            EnterUsername = '👤 Введите <b>имя пользователя</b> (для обращения через телеграм),\n' \
                            'или можете использовать текущее имя пользователя (@{})'
            ErrorEnterUsername = '😖 Введённое имя пользователя <b>превышает</b> допустимое количество символов <b>(макс. {} символа)</b>'

            SendPost = '📨 <b>Опубликовать</b> данное объявление?'

            SuccessSendPost = '😊 Объявление было успешно <b>опубликовано</b>.\n' \
                              '📬 Рассылка данного объявления запущена'



