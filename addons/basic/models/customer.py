from datetime import datetime, date, time
from lib.orm import *
from app import HTTPMethod
from config import conf


class Customer(HTTPMethod, SQLTable):
    uri = conf.sample_moduleDb_uri

    email = EmailField(identifier=True)
    nom = StringField(default='John Doe', length=150, fieldName="fullname")
    website = URLField(default="""http://localhost""", notNone=False)
    phone = PhoneField(default='+33100000000', notNone=False)
    gender = EnumField(default='male', values=["male", "femele"])
    fruit = SetField(default=["orange", "banana"], values=["orange", "banana", "apple"], notNone=False)
    pi = DecimalField(default=3.14)
    price = CurrencyField(default=39.95)
    photo = BinaryField(notNone=False, mimeTypes=['image/jpeg'])
    cm = IntField(size=3, default=180)
    birthday = DateField(default=date(1975, 12, 05), notNone=False)
    wakeup = TimeField(default=time(16, 45), notNone=False)
    theday = DateTimeField(default=datetime(1980, 05, 12, 13, 30), notNone=False)
    meeting = DateTimeField(default=datetime(2017, 12, 27, 14, 30), notNone=False)
    chomeur = BoolField(default=True)
    favoritecolor = ColorField(default='#FFFFFF')
    idx1 = Index(['chomeur', 'cm'])
    idx2 = Index('nom')
    country = ForeignKey('Country')

    @staticmethod
    def test():
        c = Customer({"aller": 13450})
        t.set("fatiguer", True)
        t.set("d", datetime.date(1943, 3, 13))
        t.set("mail", "machin@toto.fr")
