import pytest

from src.store.dao import DaoManager
from src.store.db import DataSource


@pytest.mark.dao
class TestDao(object):

    @pytest.fixture
    def data_source(self):
        return DataSource(config_section="CONFIG_QA")

    @pytest.fixture
    def dao_manager(self, data_source):
        return DaoManager(data_source)

    @pytest.fixture
    def item_dao(self, dao_manager):
        return dao_manager.get_item_dao()

    @pytest.fixture
    def order_dao(self, dao_manager):
        return dao_manager.get_order_dao()

    @pytest.fixture
    def report_dao(self, dao_manager):
        return dao_manager.get_report_dao()

    def test_order_dao_insert(self, order_dao):
        pass

    def test_item_dao_insert(self, item_dao):
        pass

    def test_report_dao_get_sales_record(self, report_dao):
        pass
