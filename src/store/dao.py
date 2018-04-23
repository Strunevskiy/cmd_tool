"""This module contains classes that save, delete and retrieve business entities from persistent store."""

from decimal import Decimal

from src.base.entity import ReportRecord, Item, TYPE, Order, User
from src.utils.file import PropertyUtil


class OrderDao(object):
    """It works with persistent store to save, retrieve and delete order details.

    Attributes:
        __data_source (DataSource): an object holding DB connection and configuration.
    """

    INSERT_ORDER = """INSERT INTO orders (seller_name) VALUES (%s)"""
    SELECT_BY_ID = """SELECT seller_name FROM orders WHERE order_id = (%s)"""
    SELECT_ALL = """SELECT order_id, seller_name FROM orders"""
    DELETE_BY_ID = """DELETE FROM orders WHERE order_id = (%s)"""

    def __init__(self, data_source):
        self.__data_source = data_source

    def persist(self, order):
        with self.__data_source.get_connection().cursor() as cursor:
            cursor.execute(self.INSERT_ORDER, order.get_user().fullname)
            order_id = cursor.lastrowid
        return order_id

    def find_by_id(self, order_id):
        with self.__data_source.get_connection().cursor() as cursor:
            cursor.execute(self.SELECT_BY_ID, order_id)
            row = cursor.fetchone()
            if row is not None:
                return Order(User().from_string(row.get("seller_name")))
            else:
                return Order()

    def find_all(self):
        orders = []
        with self.__data_source.get_connection().cursor() as cursor:
            cursor.execute(self.SELECT_ALL)
            data = cursor.fetchall()
            for row in data:
                orders.append(Order(User().from_string(row.get("seller_name")), row.get("order_id")))
            return orders

    def delete_by_id(self, order_id):
        with self.__data_source.get_connection().cursor() as cursor:
            cursor.execute(self.DELETE_BY_ID, order_id)


class ItemDao(object):
    """It works with persistent store to save and retrieve order items.

    Attributes:
        __data_source (DataSource): an object holding DB connection and configuration.
    """

    INSERT_ITEM = """INSERT INTO order_items (item_name, item_type, cost, order_id) VALUES (%s, %s, %s, %s)"""
    SELECT_BY_ITEM_ID = """SELECT item_name, item_type, cost, order_id FROM order_items WHERE item_id = (%s)"""
    SELECT_BY_ORDER_ID = """SELECT item_id, item_name, item_type, cost FROM order_items WHERE order_id = (%s)"""

    def __init__(self, data_source):
        self.__data_source = data_source

    def persist(self, item, order_id):
        with self.__data_source.get_connection().cursor() as cursor:
            params = (item.get_name(), item.get_item_type(), item.get_cost(), order_id)
            cursor.execute(self.INSERT_ITEM, params)
            item_id = cursor.lastrowid
            return item_id

    def find_by_id(self, item_id):
        with self.__data_source.get_connection().cursor() as cursor:
            cursor.execute(self.SELECT_BY_ITEM_ID, item_id)
            row = cursor.fetchone()
            if row is not None:
                return Item(row.get("item_name"), row.get("cost"), row.get("item_type"), item_id)
            else:
                return Item()


class ReportDao(object):
    """It works with persistent store to retrieve sales figures.

    Attributes:
        __data_source (DataSource): an object holding DB connection and configuration.
    """

    SELECT_RECORDS = """SELECT orders.seller_name as seller_name, COUNT(orders.seller_name) as number, SUM(order_items.cost) as value 
                        FROM orders INNER JOIN order_items on orders.order_id = order_items.order_id 
                        GROUP BY orders.seller_name"""

    def __init__(self, data_source):
        self.__data_source = data_source

    def get_sales_records(self):
        records = []
        with self.__data_source.get_connection().cursor() as cursor:
            cursor.execute(self.SELECT_RECORDS)
            data = cursor.fetchall()
            for row in data:
                records.append(ReportRecord(row.get("seller_name"), row.get("number"), row.get("value")))
            return records


class DaoManager(object):
    """It holds all of the DAO.

    Attributes:
        __data_source (DataSource): an object holding DB connection and configuration.
        __item_dao (ItemDao):
        __order_dao (OrderDao):
        __report_dao (ReportDao):
    """

    def __init__(self, data_source):
        self.__data_source = data_source
        self.__item_dao = None
        self.__order_dao = None
        self.__report_dao = None

    def get_item_dao(self):
        if self.__item_dao is None:
            self.__item_dao = ItemDao(self.__data_source)
        return self.__item_dao

    def get_order_dao(self):
        if self.__order_dao is None:
            self.__order_dao = OrderDao(self.__data_source)
        return self.__order_dao

    def get_report_dao(self):
        if self.__report_dao is None:
            self.__report_dao = ReportDao(self.__data_source)
        return self.__report_dao

    def close_connection(self):
        self.__data_source.close()

    def commit(self):
        self.__data_source.commit()


menu_storage_path = "./../resource/menu.cfg"
beverage_section = "BEVERAGE"
ingredients_section = "INGREDIENT"


class ItemDaoFile(object):

    def __init__(self):
        self.__property_util = PropertyUtil()

    def find_all_by_type(self, item_type):
        records = self.__property_util.get_entries(menu_storage_path, item_type.upper());
        items = []
        for name, cost in records:
            items.append(Item(name, Decimal(cost), item_type))
        return items

    def is_present(self, item):
        items = self.find_all_by_type(item.get_item_type())
        for name, cost in items:
            if name == item.item.get_name():
                return True
        return False

    def find_all(self):
        all_items = []
        all_items.extend(self.find_all_by_type(TYPE.BEVERAGE))
        all_items.extend(self.find_all_by_type(TYPE.ADDITION))
        return all_items
