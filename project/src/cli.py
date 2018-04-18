import logging
import traceback
from cmd import Cmd

from project.src.base.entity import POSITION, Order, Item, TYPE, User
from project.src.service.exporter import ConsoleExporter, CSVExporter
from project.src.service.service import OrderService, ReportService
from project.src.store.dao import DaoManager, ItemDaoFile
from project.src.store.db import DataSource
from project.src.service import ServiceError


class BasePrompt(Cmd):

    def __init__(self, user: User):
        super().__init__()
        self._user = user
        self._data_source = DataSource()
        self._dao_manager = DaoManager(self._data_source)

    def cmdloop(self, line):
        super().onecmd(line)
        super().cmdloop()

    def default(self, line):
        super().default(line)
        self.do_help("help")

    def get_user(self):
        return self._user

    def get_dao_manager(self):
        return self._dao_manager

    def do_quit(self, args):
        raise SystemExit

    def help_quit(self):
        print("go out of the app")

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

    _available_item_types = ["beverage", "ingredient"]

    def __init__(self, user):
        super().__init__(user)
        self._order: Order = None
        self._item_dao_file = ItemDaoFile()
        self._order_service = OrderService(self.get_dao_manager())

    def do_show(self, arg):
        self._log.info("Command show was invoked with arg: {}".format(arg))
        if arg in self._available_item_types:
            if arg == self._available_item_types[0]:
                items = self._item_dao_file.find_all_by_type(TYPE.BEVERAGE)
            elif arg == self._available_item_types[1]:
                items = self._item_dao_file.find_all_by_type(TYPE.ADDITION)
            if len(items) != 0:
                for item in items:
                    print(item.get_name())
            else:
                self._log.info("No items were found for {}.".format(arg))
                print("Nothing is available for {}.".format(arg))
        else:
            self._log.info("Command show can be invoked with args: {}".format(self._available_item_types))
            print("Command was invoked with incorrect arg.")
            self.help_show()

    def help_show(self):
        print("Command show can be invoked with one of the available args.")
        print("Available args: " + ", ".join(self._available_item_types))

    def do_price(self, arg):
        self._log.info("Command price was invoked.")
        self._log.info("Available item types: " + ", ".join(self._available_item_types))
        for item_type in self._available_item_types:
            self._log.info("Requesting items related to: " + item_type)
            items = self._item_dao_file.find_all_by_type(item_type)
            self._log.info("Requested items: " + ", ".join(items))
            self._log.info("Printing items for user.")
            for item in items:
                print("{}:{}:{}".format(item.get_name(), item.get_cost(), item.get_item_type()))
            self._log.info("Completed printing items for user.")

    def help_price(self, arg):
        print("Show price for: " + ", ".join(self._available_item_types))
        print("No args are required.")

    def do_submit_order(self, arg):
        self._log.info("Command submit_order was invoked")
        self._log.info("Order to be submitted: {}".format(str(self._order)))
        try:
            self._log.info("Creating the bill from the order.")
            self._order_service.make_bill(self._order)
            self._log.info("The bill from the order was created.")

            self._log.info("Persisting data of the order.")
            self._order_service.save(self._order)
            self._log.info("The data of the order was persisted.")
        except ServiceError as e:
            self._log.exception(e)
            print("Order was not submitted due to order service not being able to handle the order.")
        except Exception as e:
            self._log.exception(e)
            print("Order was not submitted due to unexpected things.")
        else:
            self._log.info("Order was submitted successfully. Order: {}".format(str(self._order)))
            print("Order was submitted successfully.")

    def help_submit_order(self):
        print("Submit created order.")
        print("No args are required.")

    def add_item(self, arg):
        self._log.info("Command add_item_to_order was invoked.")

        requested_items = arg.split(" ")
        self._log.info("Items requested to be added to the order: " + ", ".join(requested_items))

        if len(requested_items) == 0:
            print("No args were specified.")
            return

        available_items = self._item_dao_file.find_all()

        order_items = []
        for requested_item in requested_items:
            for available_item in available_items:
                if requested_item.lower().strip() == available_item.get_name().lower():
                    order_items.append(available_item)

        order_items_names = [order_item.get_name() for order_item in order_items]
        not_found_items = [requested_item for requested_item in requested_items if requested_item not in order_items_names]

        if len(not_found_items) == 0:
            self._log.info("All requested items were found and are ready to be added to the order.")
            self._create_order()
            self._order.add_items(order_items)
            self._log.info("Requested items were added to the order.")
            print("Provided beverage or ingredient was added to the order.")
        else:
            not_found_items_str = ", ".join(not_found_items)
            self._log.info("Requested items were not added to the order because of some not being found: " + not_found_items_str)
            print("Specified beverage or ingredient was not added to the order because of some not being found: " + not_found_items_str)
            self.help_add_item_to_order()

    def help_add_item(self):
        print("Command add_item can be invoked with args.")
        print("Args are list of beverage or ingredient names passed vie whitespace.")

    def do_clean(self, arg):
        self._log.info("Command clean was invoked.")
        if self._order is not None:
            self._order.clean_item_bunch()
            self._log.info("Order was cleaned.")
            print("Order was cleaned.")
        else:
            self._log.info("Command clean was invoked on not created order.")
            print("Order was not created.")

    def help_clean(self):
        print("Clean created order.")
        print("No args are required.")

    def _create_order(self):
        if self._order is None:
            self._order = Order()
            self._log.info("Order was created.")
        else:
            self._log.info("Order has been already created.")


class ManagerPrompt(BasePrompt):
    _log = logging.getLogger()

    _available_args_gen_report = ["console", "sheet"]

    def __init__(self, user):
        super().__init__(user)
        self._reporter_service = ReportService(self.get_dao_manager())

    def do_generate_report(self, arg):
        self._log.info("Command generate_report was invoked with arg: {}.".format(arg))
        if arg in self._available_args_gen_report:
            if arg == self._available_args_gen_report[0]:
                self._reporter_service.report(ConsoleExporter())
            elif arg == self._available_args_gen_report[1]:
                self._reporter_service.report(CSVExporter())
        else:
            print("Command was invoked with incorrect arg.")
            self.help_generate_report()

    def help_generate_report(self):
        print("Command generate_report can be invoked with one of the available args.")
        print("Available args: " + ", ".join(self._available_args_gen_report))
