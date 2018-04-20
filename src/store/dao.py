from decimal import Decimal

from src.base.entity import ReportRecord, Item, TYPE, Order, User
from src.utils.file import PropertyUtil


class OrderDao(object):
    _insert_order = """INSERT INTO orders (seller_name) VALUES (%s)"""
    _select_by_id = """SELECT seller_name FROM orders WHERE order_id = (%s)"""
    _select_by_seller = """SELECT order_id, seller_name FROM orders WHERE seller_name = (%s)"""

    def __init__(self, data_source):
        self._data_source = data_source

    def persist(self, order):
        with self._data_source.get_connection().cursor() as cursor:
            cursor.execute(self._insert_order, order.get_user().fullname)
            order_id = cursor.lastrowid
        return order_id

    def find_by_id(self, order_id):
        with self._data_source.get_connection().cursor() as cursor:
            cursor.execute(self._select_by_id, order_id)
            row = cursor.fetchone()
            if row is not None:
                return Order(User().from_string(row.get("seller_name")))
            else:
                return Order()

    def find_by_seller(self, user):
        sellers = []
        with self._data_source.get_connection().cursor() as cursor:
            cursor.execute(self._select_by_seller, user.fullname)
            data = cursor.fetchall()
            for row in data:
                sellers.append(User().from_string(row.get("seller_name")))
        return sellers


class ItemDao(object):
    _insert_item = """INSERT INTO order_items (item_name, item_type, cost, order_id) VALUES (%s, %s, %s, %s)"""
    _select_by_item_id = """SELECT item_name, item_type, cost, order_id FROM order_items WHERE item_id = (%s)"""
    _select_by_order_id = """SELECT item_id, item_name, item_type, cost FROM order_items WHERE order_id = (%s)"""

    def __init__(self, data_source):
        self._data_source = data_source

    def persist(self, item, order_id):
        with self._data_source.get_connection().cursor() as cursor:
            params = (item.get_name(), item.get_item_type(), item.get_cost(), order_id)
            cursor.execute(self._insert_item, params)
            item_id = cursor.lastrowid
            return item_id

    def find_by_item_id(self, item_id):
        with self._data_source.get_connection().cursor() as cursor:
            cursor.execute(self._select_by_item_id, item_id)
            row = cursor.fetchone()
            if row is not None:
                return Item(row.get("item_name"), row.get("cost"), row.get("item_type"), item_id)
            else:
                return Item()

    def find_all_by_order_id(self, order_id):
        items = []
        with self._data_source.get_connection().cursor() as cursor:
            cursor.execute(self._select_by_order_id, order_id)
            data = cursor.fetchall()
            for row in data:
                items.append(Item(row.get("item_name"), row.get("cost"), row.get("item_type"), row.get("item_id")))
        return items


class ReportDao(object):
    _select_records = """SELECT orders.seller_name as seller_name, COUNT(orders.seller_name) as number, SUM(order_items.cost) as value 
                        FROM orders INNER JOIN order_items on orders.order_id = order_items.order_id 
                        GROUP BY orders.seller_name"""

    def __init__(self, data_source):
        self._data_source = data_source

    def get_sales_records(self):
        records = []
        with self._data_source.get_connection().cursor() as cursor:
            cursor.execute(self._select_records)
            data = cursor.fetchall()
            for row in data:
                records.append(ReportRecord(row.get("seller_name"), row.get("number"), row.get("value")))
            return records


class DaoManager(object):

    def __init__(self, data_source):
        self._data_source = data_source
        self._item_dao = None
        self._order_dao = None
        self._report_dao = None

    def get_item_dao(self):
        if self._item_dao is None:
            self._item_dao = ItemDao(self._data_source)
        return self._item_dao

    def get_order_dao(self):
        if self._order_dao is None:
            self._order_dao = OrderDao(self._data_source)
        return self._order_dao

    def get_report_dao(self):
        if self._report_dao is None:
            self._report_dao = ReportDao(self._data_source)
        return self._report_dao

    def close_connection(self):
        self._data_source.close()

    def commit(self):
        self._data_source.commit()


menu_storage_path = "./../resource/menu.cfg"
beverage_section = "BEVERAGE"
ingredients_section = "INGREDIENT"


class ItemDaoFile(object):

    def __init__(self):
        self._property_util = PropertyUtil()

    def find_all_by_type(self, item_type):
        records = self._property_util.get_entries(menu_storage_path, item_type.upper());
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
