from typing import Union

from database.models import *


def create_tables():
    Users.create_table()
    Categories.create_table()
    Post.create_table()
    Pictures.create_table()
    PostPictures.create_table()
    logger.success('Success create all tables')


class SessionWork:
    """
        Класс для работы с сессией, взять установить значение
    """

    @staticmethod
    def get(chat_id: int, key: str):
        """
            Взять значение из сессии
        :param chat_id: айди пользователя
        :param key: ключ по которому лежит что-либо
        :return: значение под переданным ключом
        """
        return Users.get(Users.id == chat_id).session.get(key)

    @staticmethod
    def set(chat_id: int, key: str, value):
        """
            Установка нового значения в сесиию
        :param chat_id: айди пользователя
        :param key: ключ под которым будет новое значение
        :param value: новое значение
        :return:
        """
        user: Users = Users.get(Users.id == chat_id)
        session = user.session

        if '___' in key:
            # если в ключе есть ___ то делаем по ключу перед ___ словарь, в котором будет
            # ключ который расположен после ___, максимум один уровень вложенности
            key, dict_key = key.split('___')

            if session.get(key):
                session[key][dict_key] = value

            else:
                session[key] = {dict_key: value}

        else:
            session[key] = value

        user.save()


class UsersWork:
    """
        Класс для работы с сущностями пользователя
    """

    @staticmethod
    def is_registered(chat_id: int):
        return Users.get_or_none(Users.id == chat_id)

    @staticmethod
    def new_user(chat_id: int, username: str = ''):
        Users(id=chat_id,
              username=username).save(force_insert=True)

    @staticmethod
    def is_admin(chat_id: int) -> bool:
        return Users.get_by_id(chat_id).status == Constants.StatusTitles.Admin


class CategoryWork:
    """
        Класс для работы с сущностью категории
    """
    @staticmethod
    def get_category(category_id: Union[int, str]):
        return Categories.get_by_id(category_id)

    @staticmethod
    def get_categories(parent_id: Union[int, str] = None) -> list:
        return Categories.select().where(Categories.parent_id == parent_id)

    def get_all_parents(self, category_id: Union[str, int]) -> list:
        if category := Categories.get_by_id(category_id):
            categories = [category]
            if category.parent_id:
                categories += self.get_all_parents(category_id=category.parent_id)
        return categories

    def get_all_child(self, category_id: Union[str, int]):
        if category := Categories.get_by_id(category_id):
            categories = [category]
            for category in self.get_categories(parent_id=category.id):
                categories += self.get_all_child(category_id=category.id)
        return categories

    @staticmethod
    def new_category(parent_id: Union[int, str], title: str):
        Categories(parent_id=parent_id,
                   title=title).save()

    def remove_category(self, category_id: int):
        childs = self.get_all_child(category_id=category_id)
        Categories.get_by_id(category_id).delete_instance()
        for child in childs:
            child.delete_instance()

    @staticmethod
    def change_category(category_id: Union[str, int], new_title: str):
        category: Categories = Categories.get_by_id(category_id)
        category.title = new_title
        category.save()


if __name__ == '__main__':
    ...
