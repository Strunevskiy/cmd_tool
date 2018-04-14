import logging
from time import strftime, gmtime

from project.src.base.entity import Order
from project.src.exporter import Exporter
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
        try:
            order_id = self._dao_manager.get_order_dao().insert(order)
            for item in order.get_items():
                self._dao_manager.get_item_dao().insert(item, order_id)
        except Exception as e:
            self._log.error("{}".format(e))
        else:
            self._dao_manager.commit()
        finally:
            self._dao_manager.close_connection()


class ReportService(object):

    def __init__(self, dao_manager: DaoManager):
        self._dao_manager = dao_manager

    def report(self, exporter: Exporter):
        records = self._dao_manager.get_report_dao().get_sales_records()
        exporter.export(records)

