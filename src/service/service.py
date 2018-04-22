import logging

from decimal import Decimal
from time import strftime, gmtime

from src.base.entity import round_cost
from .exception import ServiceError
from src.utils.file import TemplateUtil, FileUtil


class OrderService(object):
    _log = logging.getLogger()

    _bill_date_format = "%Y-%m-%d %H:%M:%S"
    _bill_outcome_path_template = "./../outcome/{}.txt"
    _bill_template_path = "./../resource/template/bill.txt"

    def __init__(self, dao_manager):
        self._dao_manager = dao_manager

    def make_bill(self, order):
        self._log.info("Trying to make the order bill: {}.".format(order))
        if len(order.get_items()) == 0:
            raise ServiceError("There was an attempt to make the bill without items." + str(order))

        order_date = strftime(self._bill_date_format, gmtime())
        items_to_string = "\n".join([item.__str__() for item in order.get_items()])
        template_data = {"date": order_date, "user": order.get_user().fullname, "item": items_to_string}
        outcome = TemplateUtil.process_template(self._bill_template_path, template_data)
        FileUtil.write(self._bill_outcome_path_template.format(order_date), outcome)

    def save(self, order):
        self._log.info("Trying to save the order: {}.".format(order))
        if len(order.get_items()) == 0:
            raise ServiceError("There was an attempt to save the order without items." + str(order))
        try:
            self._log.debug("Persisting the order: {}.".format(order))
            order_id = self._dao_manager.get_order_dao().persist(order)
            self._log.debug("The order was persisted with order id: " + str(order_id))
            for item in order.get_items():
                self._log.debug("Persisting the item: {}.".format(item))
                item_id = self._dao_manager.get_item_dao().persist(item, order_id)
                self._log.debug("The item was persisted with item id: " + str(item_id))
        except Exception as e:
            raise e
        else:
            self._dao_manager.commit()
            logging.info("The order was committed to db.")
        finally:
            self._dao_manager.close_connection()
            logging.debug("DB connection was closed.")


class ReportService(object):
    _log = logging.getLogger()

    def __init__(self, dao_manager):
        self._dao_manager = dao_manager

    def report(self, exporter):
        try:
            self._log.info("Extracting sales records from db.")
            records = self._dao_manager.get_report_dao().get_sales_records()
        except Exception as e:
            raise e
        else:
            self._log.info("Sales records were extracted.")
            self._log.debug("Extracted sales records: %s", records)

        total_sales = 0
        total_values = 0.0000
        export_data = []
        for record in records:
            sales_number = record.get_sales_number()
            sales_value = record.get_sales_value()
            total_sales = total_sales + sales_number
            total_values = Decimal(total_values) + Decimal(sales_value)
            export_data.append((record.get_fullname(), str(sales_number), str(sales_value)))
        self._log.info("Exporting sales data.")
        self._log.debug("Sales data: \n %s", export_data)
        self._log.debug("Total sales: %s. Total cost: %s", total_sales, round_cost(total_values))
        exporter.export(export_data, str(total_sales), str(round_cost(total_values)))
        self._log.info("Exporting was completed.")


