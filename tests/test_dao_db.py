import logging

import pytest

from src.store.dao import DaoManager
from src.store.db import DataSource


@pytest.mark.dao
class TestDao(object):
    _log = logging.getLogger()

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
        pass
