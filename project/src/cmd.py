import logging
from cmd import Cmd

from project.src.base.entity import POSITION, Order, Item, TYPE
from project.src.store.db import DataSource
from project.src.exporter import ConsoleExporter, CSVExporter
from project.src.service import ReportService, OrderService
from project.src.store.dao import DaoManager, ItemDao


class BasePrompt(Cmd):

    def __init__(self, user):
        super().__init__()
        self._user = user
        self._data_source = DataSource()
        self._dao_manager = DaoManager(self._data_source)

    def get_user(self):
        return self._user

    def get_dao_manager(self):
        return self._dao_manager

    def do_quit(self, args):
        raise SystemExit

    @staticmethod
    def get_prompt(user):
        if user.get_position() == POSITION.SALESMAN:
            return SalesmanPrompt(user)
        elif user.get_position() == POSITION.MANAGER:
            return ManagerPrompt(user)
        else:
            return None


class SalesmanPrompt(BasePrompt):
    _log = logging.getLogger()

    def __init__(self, user):
        super().__init__(user)
        self._item_dao = ItemDao()

    def do_show_beverage(self, args):
        items = self._item_dao.find_all_by_type(TYPE.BEVERAGE)
        for item in items:
            print(item.get_name())

    def do_show_ingredient(self, args):
        items = self._item_dao.find_all_by_type(TYPE.ADDITION)
        for item in items:
            print(item.get_name())

    def do_get_price_by_beverage(self, args):
        return

    def do_create_order(self, args):
        return

    def do_submit_order(self, args):
        order = Order(self.get_user())

        order.add_item(Item("ddd", "20.1111", TYPE.BEVERAGE))
        order.add_item(Item("sss", "30.1111",TYPE.ADDITION))
        order.add_item(Item("aaa", "1.1111", TYPE.ADDITION))
        order.add_item(Item("ccc", "0.1111", TYPE.BEVERAGE))

        order_service = OrderService(self.get_dao_manager())
        order_service.make_bill(order)
        order_service.save(order)

    def add_ingredient(self, args):
        return

    def add_beverage(self, args):
        return

    def do_clean_order(self, args):
        return


class ManagerPrompt(BasePrompt):

    def __init__(self, user):
        super().__init__(user)
        self._reporter_service = ReportService(self.get_dao_manager())

    def do_generate_report(self, arg):
        available_arg = ["-console", "-sheet"]
        if arg:
            if arg == available_arg[0]:
                self._reporter_service.report(ConsoleExporter())
            elif arg == available_arg[1]:
                self._reporter_service.report(CSVExporter())
            else:
                print("available arg:" + ", ".join(available_arg))
        else:
            print("please input args")
