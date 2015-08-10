from lib.orm import *
from app import HTTPMethod


class Country(HTTPMethod, SQLTable):
    name = StringField(length=50)
    price = CurrencyField(default=0.00)
    paypalCode = StringField(length=2, unique=True)
    flag = ImageField(notNone=False, backendFS=True, mimeTypes=['image/jpeg', 'image/png'])

    @property
    def price(self):
        return self._price * 2

    @price.setter
    def price(self, value):
        self._price = value
