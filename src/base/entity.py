from decimal import Decimal


def round_cost(cost):
    return round(cost, 4)


class TYPE:
    def __init__(self):
        pass

    BEVERAGE = "beverage"
    ADDITION = "ingredient"


class Item(object):

    def __init__(self, name="", cost=0, item_type="", item_id=0):
        self._name = name
        self._cost = round_cost(Decimal(cost))
        self._item_type = item_type
        self._item_id = item_id

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_cost(self):
        return self._cost

    def set_cost(self, cost):
        self._cost = cost

    def get_item_type(self):
        return self._item_type

    def set_item_type(self, item_type):
        self._item_type = item_type

    def get_item_id(self):
        return self._item_id

    def set_item_id(self, item_id):
        self._item_id = item_id

    def __key(self):
        return self._name, self._cost, self._item_type, self._item_id

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return (isinstance(other, type(self)) and
                (self._name, self._cost, self._item_type, self._item_id)
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

    def __init__(self, first_name="", last_name="", position=""):
        self._first_name = first_name
        self._last_name = last_name
        self._position = position

    def set_first_name(self, first_name):
        self._first_name = first_name

    def set_last_name(self, last_name):
        self._last_name = last_name

    def set_position(self, position):
        self._position = position

    def get_first_name(self):
        return self._first_name

    def get_last_name(self):
        return self._last_name

    def get_position(self):
        return self._position

    @property
    def fullname(self):
        return "{}, {}".format(self._first_name, self._last_name)

    @fullname.setter
    def fullname(self, fullname):
        fist_name, last_name = fullname.split(", ")
        self._first_name = fist_name
        self._last_name = last_name

    @classmethod
    def from_string(cls, fullname, position=""):
        first_name, last_name = fullname.split(", ")
        return cls(first_name=first_name, last_name=last_name, position=position)

    def __repr__(self):
        return "Full name: {}. Position: {}.".format(self.fullname, self._position)

    def __str__(self):
        return self.fullname


class Order(object):

    def __init__(self, user, order_id=0):
        self._user = user
        self._order_id = order_id
        self._item_bunch = []

    def get_user(self):
        return self._user

    def set_user(self, user):
        self._user = user

    def add_items(self, *args):
        self._item_bunch.extend(args)

    def get_items(self):
        return self._item_bunch

    def clean_item_bunch(self):
        self._item_bunch.clear()

    def __repr__(self):
        return "{} {}".format(self._user.__repr__(), str(self._item_bunch))


class ReportRecord(object):

    def __init__(self, fullname, sales_number, sales_value):
        self._fullname = fullname
        self._sales_number = sales_number
        self._sales_value = round_cost(sales_value)

    def get_fullname(self):
        return self._fullname

    def get_sales_number(self):
        return self._sales_number

    def get_sales_value(self):
        return self._sales_value

    def __key(self):
        return self._fullname, self._sales_number, self._sales_value

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return (isinstance(other, type(self)) and
                (self._fullname, self._sales_number, self._sales_value)
                == (other.get_fullname(), other.get_sales_number(), other.get_sales_value()))

    def __repr__(self):
        return "fullname:{},sales:{},value:{}".format(self._fullname, self._sales_number, self._sales_value)
