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

    @staticmethod
    def add_photo(chat_id: int, file_id: str) -> int:
        user: Users = Users.get(Users.id == chat_id)
        session = user.session
        photos = session['post']['photos']
        photos.append(file_id)
        user.save()
        return len(photos)


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

    @staticmethod
    def set_admin(chat_id: int):
        user: Users = Users.get_by_id(chat_id)
        user.status = Constants.StatusTitles.Admin
        user.save()

    @staticmethod
    def get_all_users() -> list[Users]:
        return Users.select()


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


class PostWork:
    """
        Класс для работы с постами
    """

    @staticmethod
    def new_post(post_data: dict) -> int:
        post = Post(title=post_data['title'],
                    description=post_data['description'],
                    price=post_data['price'],
                    phone_number=post_data['phone_number'],
                    username=post_data['username'],
                    category_id=post_data['category_id'])

        pictures = []

        for file_id in post_data['photos']:
            picture = Pictures(file_id=file_id)
            picture.save()
            pictures.append(picture.id)

        post.save()
        post.pictures.add(pictures)
        return post.id

    @staticmethod
    def get_post(post_id: int) -> Post:
        return Post.get_by_id(post_id)

    @staticmethod
    def get_posts(category_id: Union[str, int] = None) -> list[Post]:
        first_query = (Post.category_id == category_id) if category_id else True
        return Post\
            .select()\
            .where(first_query)
            # .order_by(Post.id.desc())
            # .limit(Constants.OutputAmountPostsLimit)


if __name__ == '__main__':
    ...
