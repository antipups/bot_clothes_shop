from general_config import logger


class Constants:
    class Telegram:
        Token = '889368628:AAGO10iS0nVkRlbvQre_OpgjDG2qlEbsK4s'


class Commands:
    START = ['start']


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


class Keyboard:
    StartMenuAdmin = [[Button.StartMenuAdmin.NewPost, Button.StartMenuAdmin.Categories, Button.StartMenuAdmin.NewAdmin]]
    StartMenuUsual = [[Button.StartMenuUsual.CheckPosts, Button.StartMenuUsual.CertainPosts]]


class Messages:
    StartMenu = '👋 Добро пожаловать!\n' \
                '☝️ Выберите что хотите посмотреть'


