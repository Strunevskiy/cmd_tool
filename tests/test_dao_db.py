import random
from decimal import Decimal

import pytest

from src.base.entity import Order, User, Item, ReportRecord, TYPE, round_cost
from src.store.dao import DaoManager
from src.store.db import DataSource


@pytest.mark.dao
class TestDao(object):

    @pytest.fixture(scope="class")
    def dao_manager(self):
        dao_manager = DaoManager(DataSource(config_section="CONFIG_QA"))
        self.__delete_orders(dao_manager)
        yield dao_manager
        self.__delete_orders(dao_manager)
        dao_manager.close_connection()

    def test_order_dao_insert(self, dao_manager, valid_order):
        try:
            order_id = dao_manager.order_dao.persist(valid_order)
        except Exception as e:
            assert False, e
        else:
            dao_manager.commit()

        try:
            order_act = dao_manager.order_dao.find_by_id(order_id)
        except Exception as e:
            assert False, e

        assert order_act.user.fullname == valid_order.user.fullname, "Persisted order was not found."

    def test_item_dao_insert(self, dao_manager, valid_order):
        exp_items = []
        try:
            order_id = dao_manager.order_dao.persist(valid_order)
            for item in valid_order.items:
                item_id = dao_manager.item_dao.persist(item, order_id)
                item.item_id = item_id
                exp_items.append(item)
        except Exception as e:
            assert False, e
        else:
            dao_manager.commit()

        act_items = []
        try:
            for persisted_item in exp_items:
                item = dao_manager.item_dao.find_by_id(persisted_item.item_id)
                act_items.append(item)
        except Exception as e:
            assert False, e

        assert act_items == exp_items, "Persisted items were not found at all or partially."

    def test_report_dao_get_sales_record(self, dao_manager):
        exp_orders = self.__create_random_orders(amount=2, items=2)
        for order in exp_orders:
            try:
                order_id = dao_manager.order_dao.persist(order)
                for item in order.items:
                    dao_manager.item_dao.persist(item, order_id)
            except Exception as e:
                assert False, e
            else:
                dao_manager.commit()

        exp_report_records = []
        for exp_order in exp_orders:
            fullname = exp_order.user.fullname
            sales_number = len(exp_order.items)
            sales_value = 0.0000
            for item in exp_order.items:
                sales_value = Decimal(sales_value) + Decimal(item.cost)
            exp_report_records.append(ReportRecord(fullname, sales_number, sales_value))

        try:
            act_report_records = dao_manager.report_dao.get_sales_records()
        except Exception as e:
            assert False, e
        act_report_records = [act_report_record for act_report_record in act_report_records if
                              act_report_record in exp_report_records]

        exp_report_records.sort(key=lambda x: x.sales_value)
        act_report_records.sort(key=lambda x: x.sales_value)

        assert exp_report_records == act_report_records, "Not all the persisted sales records were returned."

    def __delete_orders(self, dao_manager):
        orders = dao_manager.order_dao.find_all()
        for order in orders:
            dao_manager.order_dao.delete_by_id(order.id)
        dao_manager.commit()

    def __create_random_orders(self, amount, items):
        orders = []
        for order_number in range(amount):
            first_name = "test_first_name_{}".format(random.randint(1, 100))
            last_name = "test_last_name_{}".format(random.randint(1, 100))
            order = Order(User(first_name, last_name))
            for item_number in range(items):
                name = "test_item_{}".format(random.randint(1, 100))
                cost = round_cost(random.uniform(0.0000, 100.000))
                item_type = random.choice([TYPE.ADDITION, TYPE.BEVERAGE])
                order.add_items(Item(name, cost, item_type))
            orders.append(order)
        return orders
