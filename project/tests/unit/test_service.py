from unittest.mock import Mock
import pytest

from project.src.service import OrderService
from project.src.store import DaoManager, DataSource
from project.src.base.entity import Order, User, POSITION, Item


@pytest.mark.service
class TestService(object):

    @pytest.fixture
    def mock_dao_manager(self):
        return Mock(spec=DaoManager(DataSource()))

    def test_order_service_save_order_with_items(self, mock_dao_manager):
        test_order = Order(User("Oleg", "Strunevskiy", POSITION.MANAGER))
        test_order.add_item(Item("1", "2", "3"))
        test_order.add_item(Item("2", "2", "2"))
        test_order.add_item(Item("4", "4", "4"))

        order_service = OrderService(mock_dao_manager)
        order_service.save(test_order)

        mock_dao_manager.get_order_dao().insert.assert_called_with(test_order)
        for item in test_order.get_items():
            mock_dao_manager.get_item_dao().insert.assert_any_call(item, mock_dao_manager.get_order_dao().insert())

        mock_dao_manager.commit.assert_called_with()
        mock_dao_manager.close_connection.assert_called_with()

    def test_order_service_save_order_without_items(self, mock_dao_manager):
        test_order = Order(User("Oleg", "Strunevskiy", POSITION.MANAGER))

        with pytest.raises(ValueError, message='Expect AttributeError if order passed to service is without items'):
            order_service = OrderService(mock_dao_manager)
            order_service.save(test_order)

    def test_report_service_report(self, mock_dao_manager):
        pass
