from unittest.mock import Mock, MagicMock, patch
import pytest

from project.src.service import OrderService
from project.src.store import DaoManager, DataSource
from project.src.base.entity import Order, User, POSITION, Item


@pytest.mark.service
class TestOrderService(object):

    @pytest.fixture
    def mock_dao_manager(self):
        return Mock(spec=DaoManager(DataSource()))

    @pytest.fixture
    def order_service(self, mock_dao_manager):
        return OrderService(mock_dao_manager)

    @pytest.fixture
    def valid_order(self):
        test_order = Order(User("Oleg", "Strunevskiy", POSITION.MANAGER))
        test_order.add_item(Item("1", "2", "3"))
        test_order.add_item(Item("2", "2", "2"))
        test_order.add_item(Item("4", "4", "4"))
        return test_order

    @pytest.fixture
    def invalid_order(self):
        return Order(User("Oleg", "Strunevskiy", POSITION.MANAGER))

    def test_save_valid_order(self, mock_dao_manager, order_service, valid_order):
        order_service.save(valid_order)

        mock_dao_manager.get_order_dao().insert.assert_called_with(valid_order)
        for item in valid_order.get_items():
            mock_dao_manager.get_item_dao().insert.assert_any_call(item, mock_dao_manager.get_order_dao().insert())

        mock_dao_manager.commit.assert_called_with()
        mock_dao_manager.close_connection.assert_called_with()

    def test_save_invalid_order(self, order_service, invalid_order):
        with pytest.raises(ValueError, message='Expect AttributeError if order passed to service is without items'):
            order_service.save(invalid_order)

    def test_save_order_with_exception_thrown_order_dao(self, mock_dao_manager, order_service, valid_order):
        mock_dao_manager.get_order_dao.side_effect = Exception('Something goes wrong')
        order_service.save(valid_order)

        mock_dao_manager.commit.assert_not_called()
        mock_dao_manager.close_connection.assert_called_with()

    def test_save_order_with_exception_thrown_item_dao(self, mock_dao_manager, order_service, valid_order):
        mock_dao_manager.get_item_dao.side_effect = Exception('Something goes wrong')
        order_service.save(valid_order)

        mock_dao_manager.commit.assert_not_called()
        mock_dao_manager.close_connection.assert_called_with()