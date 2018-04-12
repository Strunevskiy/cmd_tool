import logging

from project.src.base.entity import Order, Item, Ingredient, Beverage
from project.src.db import DataSource
from project.src.utils.file import PropertyUtil

menu_storage_path = "./resource/menu.properties"
beverage_section = "BEVERAGE"
ingredients_section = "INGREDIENT"


class OrderDao(object):
    _insert_order = """INSERT INTO orders (seller_name) VALUES ("%s")"""

    def __init__(self, data_source: DataSource):
        self._data_source = data_source

    def insert(self, order: Order) -> int:
        cursor = self._data_source.get_connection().cursor()
        cursor.execute(self._insert_order, order.get_user().fullname)
        return cursor.lastrowid


class ItemDao(object):
    _insert_item = """INSERT INTO orders (item_name, item_type, cost, order_id) VALUES ("%s", "%s", "%s", "%s")"""

    def __init__(self, data_source: DataSource):
        self._data_source = data_source

    def insert(self, item: Item, order_id: int) -> int:
        cursor = self._data_source.get_connection().cursor()
        params = (item.get_name(), item.get_type(), item.get_cost(), order_id)
        cursor.execute(self._insert_item, params)
        return cursor.lastrowid


class DaoManager(object):

    def __init__(self, data_source: DataSource):
        self._data_source = data_source
        self._item_dao = None
        self._order_dao = None

    def get_item_dao(self) -> ItemDao:
        if self._item_dao is None:
            self._item_dao = ItemDao(self._data_source)
        return self._item_dao

    def get_order_dao(self) -> OrderDao:
        if self._order_dao is None:
            self._order_dao = OrderDao(self._data_source)
        return self._order_dao

    def close_connection(self):
        self._data_source.close()

    def commit(self):
        self._data_source.commit()


class BeverageDao(object):

    def __init__(self):
        self._property_util = PropertyUtil()

    def find_all(self):
        beverages = self._property_util.get_entries(menu_storage_path, beverage_section);
        beverage_bunch = []
        for beverage in beverages:
            beverage_bunch.append(Beverage(beverage[0], beverage[1]))
        return beverage_bunch

    def is_present(self, name_beverage):
        beverages = self.find_all()
        is_present = False
        for beverage in beverages:
            name = beverage[0]
            if name == name_beverage:
                is_present = True
        return is_present


class IngredientDao(object):

    def __init__(self):
        self._property_util = PropertyUtil()

    def find_all(self):
        ingredients = self._property_util.get_entries(menu_storage_path, ingredients_section);
        ingredient_bunch = []
        for ingredient in ingredients:
            ingredient_bunch.append(Ingredient(ingredient[0], ingredient[1]))
        return ingredient_bunch

    def is_present(self, name_ingredient):
        ingredients = self.find_all()
        is_present = False
        for ingredient in ingredients:
            name = ingredient[0]
            if name == name_ingredient:
                is_present = True
        return is_present
