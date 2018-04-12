from abc import ABC, abstractmethod


class Item(ABC):

    def __init__(self, name, cost):
        self._name = name
        self._cost = cost
        super().__init__()

    def get_name(self):
        return self._name

    def get_cost(self):
        return self._cost

    def set_name(self, name):
        self._name = name

    def set_cost(self, cost):
        self._cost = cost

    @abstractmethod
    def get_type(self):
        pass

    def __str__(self):
        return "{} : {} : {}".format(self.get_name(), self.get_cost(), self.get_type())


class Beverage(Item):

    def __init__(self, name, cost):
        super().__init__(name, cost)

    def get_type(self):
        return TYPE.BEVERAGE


class Ingredient(Item):

    def __init__(self, name, cost):
        super().__init__(name, cost)

    def get_type(self):
        return TYPE.ADDITION


class User(object):

    def __init__(self, first_name, last_name, position):
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
        fist_name, last_name = fullname.split(",")
        self._first_name = fist_name.rstrip()
        self._last_name = last_name.rstrip()

    @classmethod
    def from_string(cls, user):
        first_name, last_name, position = user.split(",")
        return cls(first_name, last_name, position)

    def __str__(self):
        return self.fullname


class Order(object):

    def __init__(self, user: User):
        self._user = user
        self._item_bunch = []

    def get_user(self) -> User:
        return self._user

    def set_user(self, user: User):
        self._user = user

    def add_item(self, item: Item):
        self._item_bunch.append(item)

    def get_items(self):
        return self._item_bunch

    def clean_item_bunch(self):
        self._item_bunch.clear()

    def __str__(self):
        return self._user.__str__() + " " + self._item_bunch


class ReportRecord(object):

    def __init__(self, fullname, sales_number, sales_value):
        self._fullname = fullname
        self._sales_number = sales_number
        self._sales_value = sales_value

    def get_fullname(self):
        return self._fullname

    def get_sales_number(self):
        return self._sales_number

    def get_sales_value(self):
        return self._sales_value


class POSITION:
    SALESMAN = "salesman"
    MANAGER = "manager"


class TYPE:
    BEVERAGE = "beverage"
    ADDITION = "addition"
