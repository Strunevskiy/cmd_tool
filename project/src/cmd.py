import logging
from cmd import Cmd

from project.src.entity.base import POSITION, Order
from project.src.exporter import ConsoleExporter, SpreadSheetExporter
from project.src.repository import BeverageRepository, IngredientRepository
from project.src.service import ReportService, OrderService


class BasePrompt(Cmd):

    def __init__(self, user):
        super().__init__()
        self._user = user

    def get_user(self):
        return self._user

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
        self._order_service = OrderService()
        self._beverage_repository = BeverageRepository()
        self._ingredient_repository = IngredientRepository()

    def do_show_beverage(self, args):
        beverage_bunch = self._beverage_repository.get_beverages()
        for beverage in beverage_bunch:
            print(beverage.get_name())

    def do_show_ingredient(self, args):
        ingredient_bunch = self._ingredient_repository.get_ingredients()
        for ingredient in ingredient_bunch:
            print(ingredient.get_name())

    def do_get_price_by_beverage(self, args):
        return

    def do_create_order(self, args):
        return

    def do_submit_order(self, args):
        order = Order(self.get_user())
        self._order_service.make_bill(order)
        self._order_service.save(order)

    def add_ingredient(self, args):
        return

    def add_beverage(self, args):
        return

    def do_clean_order(self, args):
        return


class ManagerPrompt(BasePrompt):

    def __init__(self, user):
        super().__init__(user)

    def do_show_sales_records(self, args):
        reporter_service = ReportService(ConsoleExporter())
        reporter_service.report()

    def do_generate_report(self, args):
        reporter_service = ReportService(SpreadSheetExporter())
        reporter_service.report()

