"""This module is made up of classes that represent business entities."""
from decimal import Decimal


def round_cost(cost):
    """It rounds cost of item up to 4 digits.

    Args:
        cost (Decimal): cost of item

    Returns:
        Decimal: rounded cost of item up to 4 digits
    """
    return round(cost, 4)


class TYPE:
    def __init__(self):
        pass

    BEVERAGE = "beverage"
    ADDITION = "ingredient"


class Item(object):
    """Representation of a item being sold.

    Attributes:
        __name (str): item name
        __cost (Decimal): item cost
        __item_type (TYPE): item type, beverage or ingredient
        __item_id (int): id of persisted item in store
    """

    def __init__(self, name="", cost=0, item_type="", item_id=0):
        self.__name = name
        self.__cost = round_cost(Decimal(cost))
        self.__item_type = item_type
        self.__item_id = item_id

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_cost(self):
        return self.__cost

    def set_cost(self, cost):
        self.__cost = cost

    def get_item_type(self):
        return self.__item_type

    def set_item_type(self, item_type):
        self.__item_type = item_type

    def get_item_id(self):
        return self.__item_id

    def set_item_id(self, item_id):
        self.__item_id = item_id

    def __key(self):
        return self.__name, self.__cost, self.__item_type, self.__item_id

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return (isinstance(other, type(self)) and
                (self.__name, self.__cost, self.__item_type, self.__item_id)
                == (other.get_name(), other.get_cost(), other.get_item_type(), other.get_item_id()))

    def __str__(self):
        return "name : {}, price : {}, type : {}".format(self.get_name(), str(self.get_cost()), self.get_item_type())

    def __repr__(self):
        return "{} : {} : {}".format(self.get_name(), str(self.get_cost()), self.get_item_type())


class POSITION:
    def __init__(self):
        pass

    SALESMAN = "salesman"
    MANAGER = "manager"


class User(object):
    """Representation of an application user.

    Attributes:
        __first_name (str): first name of user
        __last_name (str): last name of user
        __position (POSITION): position of user, salesman or manager
    """

    def __init__(self, first_name="", last_name="", position=""):
        self.__first_name = first_name
        self.__last_name = last_name
        self.__position = position

    def set_first_name(self, first_name):
        self.__first_name = first_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def set_position(self, position):
        self.__position = position

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_position(self):
        return self.__position

    @property
    def fullname(self):
        return "{}, {}".format(self.__first_name, self.__last_name)

    @fullname.setter
    def fullname(self, fullname):
        fist_name, last_name = fullname.split(", ")
        self.__first_name = fist_name
        self.__last_name = last_name

    @classmethod
    def from_string(cls, fullname, position=""):
        first_name, last_name = fullname.split(", ")
        return cls(first_name=first_name, last_name=last_name, position=position)

    def __repr__(self):
        return "Full name: {}. Position: {}.".format(self.fullname, self.__position)

    def __str__(self):
        return self.fullname


class Order(object):
    """Representation of order being submitted by user.

    Attributes:
        __user (str): user by who the order was created
        __order_id (int): id of persisted order in store
        __item_bunch (list): items of created order
    """

    def __init__(self, user, order_id=0):
        self.__user = user
        self.__order_id = order_id
        self.__item_bunch = []

    def get_user(self):
        return self.__user

    def set_user(self, user):
        self.__user = user

    def get_id(self):
        return self.__order_id

    def set_id(self, order_id):
        self.__order_id = order_id

    def add_items(self, *args):
        self.__item_bunch.extend(args)

    def get_items(self):
        return self.__item_bunch

    def clean_item_bunch(self):
        self.__item_bunch.clear()

    def __repr__(self):
        return "{} {}".format(self.__user.__repr__(), str(self.__item_bunch))


class ReportRecord(object):
    """Representation of report record being reported.

    Attributes:
        __fullname (str): fullname of salesman
        __sales_number (int): sales number
        __sales_value (Decimal): sales value
    """

    def __init__(self, fullname, sales_number, sales_value):
        self.__fullname = fullname
        self.__sales_number = sales_number
        self.__sales_value = round_cost(sales_value)

    def get_fullname(self):
        return self.__fullname

    def get_sales_number(self):
        return self.__sales_number

    def get_sales_value(self):
        return self.__sales_value

    def __key(self):
        return self.__fullname, self.__sales_number, self.__sales_value

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return (isinstance(other, type(self)) and
                (self.__fullname, self.__sales_number, self.__sales_value) ==
                (other.get_fullname(), other.get_sales_number(), other.get_sales_value()))

    def __repr__(self):
        return "fullname:{},sales:{},value:{}".format(self.__fullname, self.__sales_number, self.__sales_value)
