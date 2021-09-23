from general_config import *


class Constants:
    DB_CONNECTION_PARAMS = {'port': 8083,
                            'user': 'root',
                            'password': 'root',
                            'database': 'bot_clothes_shop',
                            'charset': 'utf8mb4'}

    class StatusTitles:
        Admin = 'admin'
        Usual = 'usual'

    Statuses = (StatusTitles.Admin,
                StatusTitles.Usual)

    LengthCategoryTitle = 32

    LengthPostTitle = 32
    LengthPostDescription = 256
    LengthPostPrice = 10
    LengthPostPhone = 20
    LengthPostUsername = 32

    OutputAmountPostsLimit = 10

