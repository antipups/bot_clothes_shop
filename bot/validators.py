import database.util as db_util


class Validator:
    @staticmethod
    def category_title(value: str) -> bool:
        try:
            return len(value) < db_util.Constants.LengthCategoryTitle
        except:
            return False

    @staticmethod
    def post_title(value: str) -> bool:
        try:
            return len(value) < db_util.Constants.LengthPostTitle
        except:
            return False

    @staticmethod
    def post_description(value: str) -> bool:
        try:
            return len(value) < db_util.Constants.LengthPostDescription
        except:
            return False

    @staticmethod
    def post_price(value: str) -> bool:
        try:
            return len(value) < db_util.Constants.LengthPostPrice
        except:
            return False

    @staticmethod
    def post_phone_number(value: str) -> bool:
        try:
            return len(value) < db_util.Constants.LengthPostPhone
        except:
            return False

    @staticmethod
    def post_username(value: str) -> bool:
        try:
            return len(value) < db_util.Constants.LengthPostUsername
        except:
            return False
