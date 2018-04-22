import pytest

from src.base.entity import Order, User, Item, ReportRecord, TYPE
from src.store.dao import DaoManager
from src.store.db import DataSource


@pytest.mark.dao
class TestDao(object):

    @pytest.fixture(scope="class")
    def dao_manager(self):
        dao_manager = DaoManager(DataSource(config_section="CONFIG_QA"))
        yield dao_manager
        dao_manager.close_connection()

    def test_order_dao_insert(self, dao_manager, valid_order):
        try:
            order_id = dao_manager.get_order_dao().persist(valid_order)
        except Exception as e:
            assert False, e
        else:
            dao_manager.commit()

        try:
            order_act = dao_manager.get_order_dao().find_by_id(order_id)
        except Exception as e:
            assert False, e

        assert order_act.get_user().fullname == valid_order.get_user().fullname

    def test_item_dao_insert(self, dao_manager, valid_order):
        exp_items = []
        try:
            order_id = dao_manager.get_order_dao().persist(valid_order)
            for item in valid_order.get_items():
                item_id = dao_manager.get_item_dao().persist(item, order_id)
                item.set_item_id(item_id)
                exp_items.append(item)
        except Exception as e:
            assert False, e
        else:
            dao_manager.commit()

        act_items = []
        try:
            for persisted_item in exp_items:
                item = dao_manager.get_item_dao().find_by_item_id(persisted_item.get_item_id())
                act_items.append(item)
        except Exception as e:
            assert False, e

        assert act_items == exp_items

    def test_report_dao_get_sales_record(self, dao_manager):
        order_test_first = Order(User("test_1", "test_1"))
        order_test_first.add_items(Item("test_11", 1.2120, TYPE.BEVERAGE), Item("test_21", 0.2120, TYPE.ADDITION))
        order_test_second = Order(User("test_2", "test_2"))
        order_test_second.add_items(Item("test_21", 2.2120, TYPE.BEVERAGE), Item("test_22", 5.9120, TYPE.BEVERAGE))
        exp_orders = [order_test_first, order_test_second]

        for order in exp_orders:
            try:
                order_id = dao_manager.get_order_dao().persist(order)
                for item in order.get_items():
                    dao_manager.get_item_dao().persist(item, order_id)
            except Exception as e:
                assert False, e
            else:
                dao_manager.commit()

        exp_report_records = []
        for exp_order in exp_orders:
            fullname = exp_order.get_user().fullname
            sales_number = len(exp_order.get_items())
            sales_value = 0.0000
            for item in exp_order.get_items():
                sales_value = sales_value + item.get_cost()
            exp_report_records.append(ReportRecord(fullname, sales_number, sales_value))

        try:
            act_report_records = dao_manager.get_report_dao().get_sales_records()
        except Exception as e:
            assert False, e

        act_report_records = [act_report_record for act_report_record in act_report_records if act_report_record in exp_report_records]

        assert exp_report_records == act_report_records
