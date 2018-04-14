from project.src.base.entity import Order, Item, TYPE, ReportRecord
from project.src.store.db import DataSource
from project.src.utils.file import PropertyUtil


class OrderDao(object):
    _insert_order = """INSERT INTO orders (seller_name) VALUES (%s)"""

    def __init__(self, data_source: DataSource):
        self._data_source = data_source

    def insert(self, order: Order) -> int:
        with self._data_source.get_connection().cursor() as cursor:
            cursor.execute(self._insert_order, order.get_user().fullname)
            order_id = cursor.lastrowid
        return order_id


class ItemDao(object):
    _insert_item = """INSERT INTO order_items (item_name, item_type, cost, order_id) VALUES (%s, %s, %s, %s)"""

    def __init__(self, data_source: DataSource):
        self._data_source = data_source

    def insert(self, item: Item, order_id: int) -> int:
        with self._data_source.get_connection().cursor() as cursor:
            params = (item.get_name(), item.get_item_type(), item.get_cost(), order_id)
            cursor.execute(self._insert_item, params)


class ReportDao(object):
    _select_records = """SELECT orders.seller_name as seller_name, COUNT(orders.seller_name) as number, SUM(order_items.cost) as value 
                        FROM orders INNER JOIN order_items on orders.order_id = order_items.order_id 
                        GROUP BY orders.seller_name"""

    def __init__(self, data_source: DataSource):
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

    def __init__(self, data_source: DataSource):
        self._data_source = data_source
        self._item_dao = None
        self._order_dao = None
        self._report_dao = None

    def get_item_dao(self) -> ItemDao:
        if self._item_dao is None:
            self._item_dao = ItemDao(self._data_source)
        return self._item_dao

    def get_order_dao(self) -> OrderDao:
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


menu_storage_path = "./resource/menu.properties"
beverage_section = "BEVERAGE"
ingredients_section = "INGREDIENT"


def get_item_section_by_type(item_type: TYPE):
    section = None
    if item_type == TYPE.BEVERAGE:
        section = beverage_section
    elif item_type == TYPE.ADDITION:
        section = ingredients_section
    return section


class ItemDao(object):

    def __init__(self):
        self._property_util = PropertyUtil()

    def find_all_by_type(self, item_type: TYPE):
        items = self._property_util.get_entries(menu_storage_path, get_item_section_by_type(item_type));
        item_bunch = []
        for item in items:
            item_bunch.append(Item(item[0], item[1], item_type))
        return item

    def is_present(self, item: Item):
        items = self.find_all(item.get_item_type())
        is_present = False
        for item in items:
            name = item[0]
            if name == item.get_item_type():
                is_present = True
        return is_present
