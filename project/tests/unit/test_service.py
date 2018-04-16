"""Test for service."""
from unittest.mock import Mock
import pytest

from src.service import OrderService
from src.store import DaoManager, DataSource
from src.base.entity import Order, User, POSITION


@pytest.mark.service
class TestOrderService(object):

    @pytest.fixture
    def mock_dao_manager(self):
        return Mock(spec=DaoManager(DataSource()))

    def test_save(self, mock_dao_manager):
        test_order = Order(User("Oleg", "Strunevskiy", POSITION.MANAGER))

        order_service = OrderService(mock_dao_manager)
        order_service.save(test_order)
        mock_dao_manager.get_order_dao().insert().assert_called_with(test_order)
