import database.util as db_util


class Validator:
    @staticmethod
    def category_title(value: str) -> bool:
        return len(value) < db_util.Constants.LengthCategoryTitle
