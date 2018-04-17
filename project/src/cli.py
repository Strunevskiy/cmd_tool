import argparse
import logging
from cmd import Cmd

from project.src.base.entity import POSITION, Order, Item, TYPE
from project.src.service.service import OrderService, ReportService
from project.src.store.db import DataSource
from project.src.service.exporter import ConsoleExporter, CSVExporter
from project.src.store.dao import DaoManager, ItemDao, ItemDaoFile


def parse(args):
    return args.split(" ")


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
        self._item_dao_file = ItemDaoFile()
        self._order: Order = None

    def do_show(self, args):
        args_cli = parse(args)
        args_command_show = ["-beverage", "-ingredient", "-all"]

        if len(args_cli) == 1:
            arg = args_cli[0]
            if arg in args_command_show:

                if arg == args_command_show[0]:
                    items = self._item_dao_file.find_all_by_type(TYPE.BEVERAGE)
                elif arg == args_command_show[1]:
                    items = self._item_dao_file.find_all_by_type(TYPE.ADDITION)
                elif arg == args_command_show[2]:
                    items = [*self._item_dao_file.find_all_by_type(TYPE.BEVERAGE),
                             *self._item_dao_file.find_all_by_type(TYPE.ADDITION)]
                if len(items) != 0:
                    for item in items:
                        print(item.get_name())

            else:
                print("Available args: " + ", ".join(args_command_show))

        else:
            print("Number of arguments can not be more that 1!")

    def help_show(self):
        print("fsdfsdf")

    def do_price(self, args):
        return

    def do_submit_order(self, args):
        order = Order(self.get_user())

        order.add_item(Item("ddd", "20.1111", TYPE.BEVERAGE))
        order.add_item(Item("sss", "30.1111", TYPE.ADDITION))
        order.add_item(Item("aaa", "1.1111", TYPE.ADDITION))
        order.add_item(Item("ccc", "0.1111", TYPE.BEVERAGE))

        order_service = OrderService(self.get_dao_manager())
        order_service.make_bill(order)
        order_service.save(order)

    def add(self, args):
        return

    def do_clean(self):
        if self._order is not None:
            self._order.clean_item_bunch()
            print("Order was cleaned.")
        else:
            print("Order was not created.")


class ManagerPrompt(BasePrompt):

    def __init__(self, user):
        super().__init__(user)
        self._reporter_service = ReportService(self.get_dao_manager())

    def do_generate_report(self, arg):
        console, sheet = ["-console", "-sheet"]
        if arg == console:
            self._reporter_service.report(ConsoleExporter())
        elif arg == sheet:
            self._reporter_service.report(CSVExporter())
        else:
            print("Available args: " + ", ".join((console, sheet)))
