class TradeAction(object):
    _price = 0
    _amount = 0
    _datetime = None
    _id = 0
    _order_type = 0

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = value

    @property
    def amount(self):
        return self.amount

    @amount.setter
    def amount(self, value):
        self._amount = value

    @property
    def datetime(self):
        return self._datetime

    @datetime.setter
    def datetime(self, value):
        self._datetime = value

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def order_type(self):
        return self._order_type

    @order_type.setter
    def order_type(self, value):
        self._order_type = value
