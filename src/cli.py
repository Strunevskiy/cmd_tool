from __future__ import print_function

import logging
from cmd import Cmd

from src.base.entity import POSITION, TYPE, Order
from src.service.exception import ServiceError
from src.service.exporter import ConsoleExporter, CSVExporter
from src.service.service import OrderService, ReportService
from src.store.dao import DaoManager, ItemDaoFile
from src.store.db import DataSource

logger = logging.getLogger()


class BasePrompt(Cmd):
    # intro = "Welcome to the coffee for mee shell.\nType help or ? to list commands.\n"
    prompt = ">>"

    def __init__(self, user):
        Cmd.__init__(self)
        self.__user = user
        self.__data_source = DataSource()
        self.__dao_manager = DaoManager(self.__data_source)

    def cmdloop(self, line):
        Cmd.onecmd(self, line)
        Cmd.cmdloop(self)
        pass

    def default(self, line):
        Cmd(self).default(line)
        self.do_help("help")

    def get_user(self):
        return self.__user

    def get_dao_manager(self):
        return self.__dao_manager

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

    __available_item_types = ["beverage", "ingredient"]

    def __init__(self, user):
        BasePrompt.__init__(self, user)
        self.__order = None
        self.__item_dao_file = ItemDaoFile()
        self.__order_service = OrderService(self.get_dao_manager())

    def do_show(self, arg):
        logger.info("Command show was invoked with arg: {}".format(arg))
        if arg in self.__available_item_types:
            if arg == self.__available_item_types[0]:
                items = self.__item_dao_file.find_all_by_type(TYPE.BEVERAGE)
            elif arg == self.__available_item_types[1]:
                items = self.__item_dao_file.find_all_by_type(TYPE.ADDITION)
            if len(items) != 0:
                for item in items:
                    print(item.get_name())
            else:
                logger.info("No items were found for {}.".format(arg))
                print("Nothing is available for {}.".format(arg))
        else:
            logger.info("The arg show command was invoked is incorrect.")
            logger.info("The available args: " + ", ".join(self.__available_item_types))
            print("Command show was invoked with incorrect args.")
            self.help_show()

    def help_show(self):
        print("Command show can be invoked with one of the available args.")
        print("Available args: " + ", ".join(self.__available_item_types))

    def do_price(self, arg):
        logger.info("Command price was invoked.")
        logger.info("Available item types: " + ", ".join(self.__available_item_types))
        for arg in self.__available_item_types:
            logger.info("Requesting items related to: " + arg)
            items = self.__item_dao_file.find_all_by_type(arg)
            logger.info("Requested items: " + ", ".join([item.__repr__() for item in items]))
            logger.info("Printing items for user.")
            for item in items:
                print(item)
                logger.info("Completed printing items for user.")

    def help_price(self, arg):
        print("Show price for: " + ", ".join(self.__available_item_types))
        print("No args are required.")

    def do_submit_order(self, arg):
        logger.info("Command submit_order was invoked")
        logger.info("Order to be submitted: {}".format(str(self.__order)))
        try:
            logger.info("Creating the bill from the order.")
            self.__order_service.make_bill(self.__order)
            logger.info("The bill from the order was created.")

            logger.info("Persisting data of the order.")
            self.__order_service.save(self.__order)
            logger.info("The data of the order was persisted.")
        except ServiceError as e:
            logger.exception(e)
            print("Order was not submitted due to order service not being able to handle the order.")
            print("The possible root cause: " + str(e))
        except Exception as e:
            logger.exception(e)
            print("Order was not submitted due to unexpected things.")
        else:
            logger.info("Order was submitted successfully. Order: {}".format(str(self.__order)))
            print("Order was submitted successfully.")
        finally:
            self.__order = None

    def help_submit_order(self):
        print("Submit the created order.")
        print("No args are required.")

    def do_add_items(self, arg):
        logger.info("Command add_item was invoked.")

        requested_items = arg.split(" ")
        logger.info("Items requested to be added to the order: " + ", ".join(requested_items))

        if len(requested_items) == 0:
            print("No args were specified.")
            self.help_add_items()
            return

        available_items = self.__item_dao_file.find_all()

        order_items = []
        for requested_item in requested_items:
            for available_item in available_items:
                if requested_item.lower().strip() == available_item.get_name().lower():
                    order_items.append(available_item)

        order_items_names = [order_item.get_name() for order_item in order_items]
        not_found_items = [requested_item for requested_item in requested_items if requested_item not in order_items_names]

        if len(not_found_items) == 0:
            logger.info("All requested items were found and are ready to be added to the order.")
            self.__create_order()
            self.__order.add_items(*order_items)
            logger.info("Requested items were added to the order.")
            print("Provided beverage or ingredient was added to the order.")
        else:
            not_found_items_str = ", ".join(not_found_items)
            logger.info("Requested items were not added to the order because of some not being found: " + not_found_items_str)
            print("Specified beverage or ingredient was not added to the order because of some not being found: " + not_found_items_str)
            self.help_add_items()

    def help_add_items(self):
        print("Command add_item can be invoked with args.")
        print("Args are list of beverage or ingredient names passed vie whitespace.")

    def do_clean(self, arg):
        logger.info("Command clean was invoked.")
        if self.__order is not None:
            self.__order.clean_item_bunch()
            logger.info("Order was cleaned.")
            print("Order was cleaned.")
        else:
            logger.info("Command clean was invoked on not created order.")
            print("Order was not created yet.")

    def help_clean(self):
        print("Clean created order.")
        print("No args are required.")

    def __create_order(self):
        if self.__order is None:
            self.__order = Order(self.get_user())
            logger.info("Order was created.")
        else:
            logger.info("Order has been already created.")


class ManagerPrompt(BasePrompt):
    __log = logging.getLogger()

    _available_args_gen_report = ["console", "sheet"]

    def __init__(self, user):
        BasePrompt.__init__(self, user)
        self.__reporter_service = ReportService(self.get_dao_manager())

    def do_generate_report(self, arg):
        logger.info("Command generate_report was invoked with arg: {}.".format(arg))
        if arg in self._available_args_gen_report:
            try:
                if arg == self._available_args_gen_report[0]:
                    logger.info("Generating report into console.")
                    self.__reporter_service.report(ConsoleExporter())
                elif arg == self._available_args_gen_report[1]:
                    logger.info("Generating report into CSV.")
                    self.__reporter_service.report(CSVExporter())
            except Exception as e:
                logger.exception(e)
                print("Report was not generated due to unexpected things.")
            else:
                logger.info("Report was generated successfully")
        else:
            print("Command was invoked with incorrect arg.")
            self.help_generate_report()

    def help_generate_report(self):
        print("Command generate_report can be invoked with one of the available args.")
        print("Available args: " + ", ".join(self._available_args_gen_report))
