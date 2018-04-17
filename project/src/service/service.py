import logging
from decimal import Decimal
from time import strftime, gmtime

from project.src.base.entity import Order
from project.src.service.exporter import Exporter
from project.src.store.dao import DaoManager
from project.src.utils.file import TemplateUtil, FileUtil


class OrderService(object):
    _log = logging.getLogger()

    _bill_date_format = "%Y-%m-%d %H:%M:%S"
    _bill_outcome_path_template = "./outcome/{}.txt"
    _bill_template_path = "./resource/template/bill.txt"

    def __init__(self, dao_manager: DaoManager):
        self._dao_manager = dao_manager

    def make_bill(self, order: Order):
        order_date = strftime(self._bill_date_format, gmtime())

        item_bunch = [item.__str__() for item in order.get_items()]
        items_to_string = "\n".join(item_bunch)

        template_data = {"date": order_date, "user": order.get_user().fullname, "item": items_to_string}
        outcome = TemplateUtil.process_template(self._bill_template_path, template_data)
        FileUtil.write(self._bill_outcome_path_template.format(order_date), outcome)

    def save(self, order: Order):
        logging.info("Trying to save the order: {}.".format(order))
        if len(order.get_items()) == 0:
            raise ValueError("There was an attempt to save the order without items." + str(order))
        try:
            order_id = self._dao_manager.get_order_dao().insert(order)
            for item in order.get_items():
                self._dao_manager.get_item_dao().insert(item, order_id)
        except Exception as e:
            self._log.error("The order was not save due to {}. Order representation {}.".format(e, str(order)))
        else:
            logging.info("Starting committing the order to db.".format(order))
            self._dao_manager.commit()
            logging.info("Committed the order to db.".format(order))
        finally:
            logging.info("Closing connection after committing the order to db.".format(order))
            self._dao_manager.close_connection()
            logging.info("Closed connection after committing the order to db.".format(order))


class ReportService(object):
    _log = logging.getLogger()

    def __init__(self, dao_manager: DaoManager):
        self._dao_manager = dao_manager

    def report(self, exporter: Exporter):
        records = self._dao_manager.get_report_dao().get_sales_records()
        total_sales = 0
        total_values = 0.0000
        export_data = []
        for record in records:
            sales_number = record.get_sales_number()
            sales_value = record.get_sales_value()
            total_sales += sales_number
            total_values = Decimal(total_values) + Decimal(sales_value)
            export_data.append((record.get_fullname(), str(sales_number), str(sales_value)))
        exporter.export(export_data, total_sales, total_values)

