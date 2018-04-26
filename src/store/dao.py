"""This module contains classes that save, delete and retrieve business entities from persistent store."""
import logging
from decimal import Decimal

from src.base.entity import ReportRecord, Item, TYPE, Order, User
from src.utils.file import PropertyUtil

logger = logging.getLogger()


class OrderDao(object):
    """It works with persistent store to save, retrieve and delete order details.

    Attributes:
        __data_source (DataSource): an object holding DB connection and configuration.
    """

    INSERT_ORDER = "INSERT INTO orders (seller_name) VALUES (%s)"
    SELECT_BY_ID = "SELECT seller_name FROM orders WHERE order_id = (%s)"
    SELECT_ALL = "SELECT order_id, seller_name FROM orders"
    DELETE_BY_ID = "DELETE FROM orders WHERE order_id = (%s)"

    def __init__(self, data_source):
        self.__data_source = data_source

    def persist(self, order):
        """It saves order details in persistent store.

        Args:
            order (Order): order to persist.

        Returns:
            int: id of persisted order.
        """
        logger.info("Persisting order: " + repr(order))
        with self.__data_source.get_connection().cursor() as cursor:
            cursor.execute(self.INSERT_ORDER, order.user.fullname)
            order_id = cursor.lastrowid
        logger.info("Persisted order id: " + str(order_id))
        return order_id

    def find_by_id(self, order_id):
        """It finds order by provided order id.

        Args:
            order_id (int): id of persisted order.

        Returns:
            Order: found order by provided order id.
        """
        logger.info("Looking for order by id: " + str(order_id))
        with self.__data_source.get_connection().cursor() as cursor:
            cursor.execute(self.SELECT_BY_ID, order_id)
            row = cursor.fetchone()
            if row is not None:
                logger.info("Order was found.")
                return Order(User().from_string(row.get("seller_name")))
            else:
                logger.info("Order was not found.")
                return Order(User())

    def find_all(self):
        """It finds all the orders in store.


        Returns:
            list: bunch of available orders in store, otherwise empty list.
        """
        logger.info("Looking for all existing orders.")
        orders = []
        with self.__data_source.get_connection().cursor() as cursor:
            cursor.execute(self.SELECT_ALL)
            data = cursor.fetchall()
            for row in data:
                orders.append(Order(User().from_string(row.get("seller_name")), row.get("order_id")))
        logger.info("There was found the following number of orders: " + str(len(orders)))
        return orders

    def delete_by_id(self, order_id):
        """It deletes order by provided order id.
        """
        logger.info("Deleting the order that has id: " + str(order_id))
        with self.__data_source.get_connection().cursor() as cursor:
            cursor.execute(self.DELETE_BY_ID, order_id)
        logger.info("The order was removed from persistent store.")


class ItemDao(object):
    """It works with persistent store to save and retrieve order items.

    Attributes:
        __data_source (DataSource): an object holding DB connection and configuration.
    """

    INSERT_ITEM = "INSERT INTO order_items (item_name, item_type, cost, order_id) VALUES (%s, %s, %s, %s)"
    SELECT_BY_ITEM_ID = "SELECT item_name, item_type, cost, order_id FROM order_items WHERE item_id = (%s)"
    SELECT_BY_ORDER_ID = "SELECT item_id, item_name, item_type, cost FROM order_items WHERE order_id = (%s)"

    def __init__(self, data_source):
        self.__data_source = data_source

    def persist(self, item, order_id):
        """It saves item in persistent store that is related to order id.

        Args:
            item (Item): item to persist.
            order_id (int): order id that item belongs to.

        Returns:
            int: persisted item id
        """
        logger.info("Order id of persisted item: " + str(order_id))
        logger.info("Persisting item: " + repr(item))
        with self.__data_source.get_connection().cursor() as cursor:
            params = (item.name, item.item_type, item.cost, order_id)
            cursor.execute(self.INSERT_ITEM, params)
            item_id = cursor.lastrowid
        logger.info("Persisted item id: " + str(item_id))
        return item_id

    def find_by_id(self, item_id):
        """It finds item by provided item id.

        Args:
            item_id (int): id of persisted item.

        Returns:
            Item: found item by provided item id, otherwise empty item
        """
        logger.info("Looking for item by item id: " + str(item_id))
        with self.__data_source.get_connection().cursor() as cursor:
            cursor.execute(self.SELECT_BY_ITEM_ID, item_id)
            row = cursor.fetchone()
            if row is not None:
                logger.info("The item was found.")
                return Item(row.get("item_name"), row.get("cost"), row.get("item_type"), item_id)
            else:
                logger.info("The item was not found.")
                return Item()


class ReportDao(object):
    """It works with persistent store to retrieve sales figures.

    Attributes:
        __data_source (DataSource): an object holding DB connection and configuration.
    """

    SELECT_RECORDS = """SELECT orders.seller_name as seller_name, COUNT(orders.seller_name) as number, 
                        SUM(order_items.cost) as value 
                        FROM orders INNER JOIN order_items on orders.order_id = order_items.order_id 
                        GROUP BY orders.seller_name"""

    def __init__(self, data_source):
        self.__data_source = data_source

    def get_sales_records(self):
        """It executes an aggregation query and returns bunch of ReportRecord object.

        Returns:
            list: bunch of ReportRecord object
        """
        logger.info("Collecting sales figures.")
        records = []
        with self.__data_source.get_connection().cursor() as cursor:
            cursor.execute(self.SELECT_RECORDS)
            data = cursor.fetchall()
            for row in data:
                records.append(ReportRecord(row.get("seller_name"), row.get("number"), row.get("value")))
        logger.info("The number of sales figures was collected.")
        return records


class DaoManager(object):
    """It holds all of the DAO allowing to do operations from different DAO in one transaction.

    Attributes:
        __data_source (DataSource): an object holding DB configuration and connection.
        __item_dao (ItemDao): an object providing access to item
        __order_dao (OrderDao): an object providing access to order
        __report_dao (ReportDao): an object providing access to sales figures
    """

    def __init__(self, data_source):
        self.__data_source = data_source
        self.__item_dao = None
        self.__order_dao = None
        self.__report_dao = None

    @property
    def item_dao(self):
        """It initializes ItemDao if has not been initialized yet and returns it.

        Returns:
            ItemDao: an object responsible for providing access to items in DB.
        """
        if self.__item_dao is None:
            self.__item_dao = ItemDao(self.__data_source)
        return self.__item_dao

    @property
    def order_dao(self):
        """It initializes OrderDao if has not been initialized yet and returns it.

        Returns:
            OrderDao: an object responsible for providing access to orders in DB.
        """
        if self.__order_dao is None:
            self.__order_dao = OrderDao(self.__data_source)
        return self.__order_dao

    @property
    def report_dao(self):
        """It initializes ReportDao if has not been initialized yet and returns it.

        Returns:
            ReportDao: an object responsible for providing access to report records in DB.
        """
        if self.__report_dao is None:
            self.__report_dao = ReportDao(self.__data_source)
        return self.__report_dao

    def close_connection(self):
        """It closes DB connection.
        """
        self.__data_source.close()

    def commit(self):
        """It commits changes to DB.
        """
        self.__data_source.commit()


menu_storage_path = "./../resource/menu.cfg"
beverage_section = "BEVERAGE"
ingredients_section = "INGREDIENT"


class ItemDaoFile(object):
    """It works with persistent store to retrieve item available to salesman.

    Attributes:
        __property_util (PropertyUtil): Interface allowing to work with persistent store.
    """

    def __init__(self):
        self.__property_util = PropertyUtil()

    def find_all_by_type(self, item_type):
        """It finds all the available items by provided item type.

        Args:
            item_type (str): item type of item to obtain.

        Returns:
            list: found items by provided item_type, otherwise empty list
        """
        logger.info("Extracting items from a file store of type: " + item_type)
        records = self.__property_util.get_entries(menu_storage_path, item_type.upper())
        logger.info("There was found the following number: " + str(len(records)))
        items = []
        for name, cost in records:
            items.append(Item(name, Decimal(cost), item_type))
        return items

    def find_all(self):
        """It obtains all the available items.

        Returns:
            list: all the available items.
        """
        all_items = []
        all_items.extend(self.find_all_by_type(TYPE.BEVERAGE))
        all_items.extend(self.find_all_by_type(TYPE.ADDITION))
        return all_items
