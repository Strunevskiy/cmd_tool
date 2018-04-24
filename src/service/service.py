"""This module contains classes that are responsible for performing different operations over business entities."""
import logging

from decimal import Decimal
from datetime import datetime

from src.base.entity import round_cost
from .exception import ServiceError
from src.utils.file import TemplateUtil, FileUtil

logger = logging.getLogger()


class OrderService(object):
    """It does different operations over order object.

    It makes the bill of order as well as saves order details to persistent storage.

    Attributes:
        __dao_manager (DaoManager): an object holding DAO for all business entities.
    """

    BILL_DATA_FORMAT = "%Y-%m-%d %H:%M:%S"
    BILL_TEMPLATE_PATH = "./../resource/template/bill.txt"
    BILL_OUTCOME_PATH_TEMPLATE = "./../outcome/{}.txt"

    def __init__(self, dao_manager):
        self.__dao_manager = dao_manager

    def make_bill(self, order):
        """It makes the bill from provided order object.

        Args:
            order (Order): an object from which the bill is created.

        Raises:
            ServiceError: if provided order does not contain items.
        """
        logger.info("Trying to make the order bill: {}.".format(order))
        if len(order.get_items()) == 0:
            raise ServiceError("There was an attempt to make the bill without items." + str(order))
        order_date = datetime.now().strftime(self.BILL_DATA_FORMAT)
        items_to_string = "\n".join([item.__str__() for item in order.get_items()])
        template_data = {"date": order_date, "user": order.get_user().fullname, "item": items_to_string}
        outcome = TemplateUtil.process(self.BILL_TEMPLATE_PATH, template_data)
        FileUtil.write(self.BILL_OUTCOME_PATH_TEMPLATE.format(order_date), outcome)

    def save(self, order):
        """It saves order in persistent storage in one transaction.

        Args:
            order (Order): an object to save.

        Raises:
            ServiceError: if provided order does not contain items.
            Exception: if order can not be persisted due to exception in dao layer.
        """
        logger.info("Trying to save the order: {}.".format(order))
        if len(order.get_items()) == 0:
            raise ServiceError("There was an attempt to save the order without items." + str(order))
        try:
            logger.info("Persisting the order: {}.".format(order))
            order_id = self.__dao_manager.get_order_dao().persist(order)
            logger.info("The order was persisted with order id: " + str(order_id))
            for item in order.get_items():
                logger.info("Persisting the item: {}.".format(item))
                item_id = self.__dao_manager.get_item_dao().persist(item, order_id)
                logger.info("The item was persisted with item id: " + str(item_id))
        except Exception as e:
            raise e
        else:
            self.__dao_manager.commit()
            logger.info("The order was committed to DB.")
        finally:
            self.__dao_manager.close_connection()
            logger.info("DB connection was closed.")


class ReportService(object):
    """It does different operations for reporting needs.

    It extracts sales records from a persistent store

    Attributes:
        __dao_manager (DaoManager): an object holding DAO for all business entities.
    """

    def __init__(self, dao_manager):
        self.__dao_manager = dao_manager

    def report(self, exporter):
        """It extracts sales details from persistent storage and exports it by using export interface.

        Args:
            exporter (Exporter): interface of exporting sales figures.

        Raises:
            AttributeError: if provided arg object does not implement Exporter interface.
        """
        try:
            logger.info("Extracting sales records from db.")
            records = self.__dao_manager.get_report_dao().get_sales_records()
        except Exception as e:
            raise e
        else:
            logger.info("Sales records were extracted.")
            logger.debug("Extracted sales records: %s", records)

        total_sales = 0
        total_values = 0.0000
        export_data = []
        for record in records:
            sales_number = record.get_sales_number()
            sales_value = record.get_sales_value()
            total_sales = total_sales + sales_number
            total_values = Decimal(total_values) + Decimal(sales_value)
            export_data.append((record.get_fullname(), str(sales_number), str(sales_value)))
        logger.debug("Sales data: \n %s", export_data)
        logger.debug("Total sales: %s. Total cost: %s", total_sales, round_cost(total_values))

        try:
            logger.info("Exporting sales data.")
            exporter.export(export_data, str(total_sales), str(round_cost(total_values)))
        except AttributeError as e:
            raise e
        else:
            logger.info("Exporting was completed.")
