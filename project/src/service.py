from time import strftime, gmtime

from project.src.base.entity import Order
from project.src.utils.file import TemplateUtil, FileUtil


class OrderService(object):
    _bill_date_format = "%Y-%m-%d %H:%M:%S"
    _bill_outcome_path_template = "./outcome/{}.txt"
    _bill_template_path = "./resource/template/bill.txt"

    def make_bill(self, order: Order):
        order_date = strftime(self._bill_date_format, gmtime())

        items = order.get_items()
        item_bunch = [item.__str__() for item in items]

        template_placeholders = {"date": order_date, "user": order.get_user().fullname, "item": "\n".join(item_bunch)}
        filled_template = TemplateUtil.process_template(self._bill_template_path, template_placeholders)

        FileUtil.write(self._bill_outcome_path_template.format(order_date), filled_template)

    def save(self, order: Order):
        pass


class ReportService(object):

    def __init__(self, exporter):
        self._exporter = exporter

    def report(self):
        self._exporter.export()
