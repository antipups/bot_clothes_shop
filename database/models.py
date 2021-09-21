from playhouse.shortcuts import ReconnectMixin
from database.config import *
import peewee
from playhouse.mysql_ext import JSONField


class ReconnectMySQLDatabase(ReconnectMixin, peewee.MySQLDatabase):
    """
        Класс для переподключения к бд если подключение упало
    """
    pass


db = ReconnectMySQLDatabase(**Constants.DB_CONNECTION_PARAMS)


class BaseModel(peewee.Model):
    """
        Базовая модель с нужным наследником и коннекшином
    """
    class Meta:
        database = db


class Users(BaseModel):
    """
        Пользователи, их данные, сессия, юзернейм, имя, телефон
    """
    class Meta:
        primary_key = False

    id = peewee.IntegerField(primary_key=True,
                             help_text='Айди пользователя в системе и в телеграмме')
    session = JSONField(default={},
                        help_text='Временные данные пользователя '
                                  '(чтоб при резете не сбрасывались некоторые формы допустим)')
    username = peewee.CharField(max_length=64,
                                help_text='Юзернейм пользователя (чтоб была возможность обратится к нему в телеграмме)',
                                null=True)
    status = peewee.CharField(choices=Constants.Statuses,
                              help_text='статус пользователя',
                              default=Constants.StatusTitles.Usual)


class Categories(BaseModel):
    """
        Категории
    """
    parent_id = peewee.IntegerField(null=True,
                                    help_text='Айди категории (если это подкатегория)')
    title = peewee.CharField(max_length=Constants.LengthCategoryTitle,
                             help_text='Название категории')
    description = peewee.TextField(null=True,
                                   help_text='Описание категории, возможно будет не использоваться в боте')


class Pictures(BaseModel):
    """
        Таблица с картинками
    """
    image = peewee.CharField(max_length=256,
                             help_text='FILE ID в телеграмме')


class Post(BaseModel):
    """
        Посты в боте
    """
    category_id = peewee.ForeignKeyField(Categories,
                                         on_delete='CASCADE',
                                         help_text='Категория продукта')
    title = peewee.CharField(max_length=255,
                             help_text='Название объявления')
    description = peewee.TextField(help_text='Описание продукта')
    price = peewee.CharField(help_text='цена за товар, цифра и валюта',
                             max_length=255)
    pictures = peewee.ManyToManyField(Pictures,
                                      backref='posts',
                                      on_delete='CASCADE')


PostPictures = Post.pictures.get_through_model()
