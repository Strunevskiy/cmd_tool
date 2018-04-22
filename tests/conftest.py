import pytest
from src.base.entity import Order, Item, User, POSITION, TYPE


@pytest.fixture(scope="session")
def valid_order():
    test_order = Order(User("Aleh", "Struneuski", POSITION.SALESMAN))
    test_order.add_items(Item("late", 6.5013, TYPE.ADDITION), Item("espresso", 2.3493, TYPE.BEVERAGE))
    return test_order


@pytest.fixture(scope="session")
def invalid_order():
    return Order(User("Aleh", "Struneuski", POSITION.SALESMAN))
