class TYPE:
    BEVERAGE = "beverage"
    ADDITION = "addition"


class Item(object):

    def __init__(self, name, cost, item_type: TYPE):
        self._name = name
        self._cost = cost
        self._item_type = item_type

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_cost(self):
        return self._cost

    def set_cost(self, cost):
        self._cost = cost

    def get_item_type(self) -> TYPE:
        return self._item_type

    def set_item_type(self, item_type: TYPE):
        self._item_type = item_type

    def __repr__(self):
        return "{} : {} : {}".format(self.get_name(), self.get_cost(), self.get_item_type())


class POSITION:
    SALESMAN = "salesman"
    MANAGER = "manager"


class User(object):

    def __init__(self, first_name: str, last_name: str, position: POSITION):
        self._first_name = first_name
        self._last_name = last_name
        self._position = position

    def set_first_name(self, first_name: str):
        self._first_name = first_name

    def set_last_name(self, last_name: str):
        self._last_name = last_name

    def set_position(self, position: POSITION):
        self._position = position

    def get_first_name(self) -> str:
        return self._first_name

    def get_last_name(self) -> str:
        return self._last_name

    def get_position(self) -> str:
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

    def __repr__(self):
        return "Full name: {}. Position: {}.".format(self.fullname, self._position)

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
        self._sales_value = sales_value

    def get_fullname(self):
        return self._fullname

    def get_sales_number(self):
        return self._sales_number

    def get_sales_value(self):
        return self._sales_value

    def __str__(self):
        return self._fullname + " " + str(self._sales_number) + " " + str(self._sales_value)
