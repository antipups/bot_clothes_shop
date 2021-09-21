from database.models import *


def create_tables():
    Users.create_table()
    Categories.create_table()
    Post.create_table()
    Pictures.create_table()
    PostPictures.create_table()
    logger.success('Success create all tables')


def is_registered(chat_id: int):
    return Users.get_or_none(Users.id == chat_id)


def new_user(chat_id: int, username: str = ''):
    Users(id=chat_id,
          username=username).save(force_insert=True)


def is_admin(chat_id: int) -> bool:
    return Users.get_by_id(chat_id).status == Constants.StatusTitles.Admin


if __name__ == '__main__':
    ...
