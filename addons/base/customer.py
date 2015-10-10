from lib.orm.models import *
from app import api


class Customer(dummy.ORM):
    # Model definition #

    email = EmailField(identifier=True)
    nom = StringField(default='John Doe', length=150, fieldName="fullname")
    website = UrlField(default="""http://localhost""", require=False)
    phone = PhoneField(default='+33100000000', require=False)
    gender = EnumField(default='femele', values=["male", "femele"], onchange='genderChange')
    fruit = SetField(default=["orange", "banana"], values=["orange", "banana", "apple"], require=False)
    pi = DecimalField(default=3.14)
    price = CurrencyField(default=39.95)
    photo = BinaryField(require=False, mimeTypes=['image/jpeg'])
    cm = IntField(size=3, default=180, constraints='sizeConstraints')
    birthday = DateField(require=False)
    # birthday = DateField(default=date(1975, 12, 05), require=False)
    age = IntField(compute='ageCompute')
    man = IntField(compute='manCompute')
    wakeup = TimeField(default=time(16, 45), require=False)
    theday = DatetimeField(default=datetime(1980, 05, 12, 13, 30), require=False)
    meeting = DatetimeField(default=datetime(2017, 12, 27, 14, 30), require=False)
    chomeur = BoolField(default=True)
    favoritecolor = ColorField(default='#FFFFFF')
    idx1 = Index(['chomeur', 'cm'])
    idx2 = Index('nom')
    # country = ForeignKey('Country')

    @staticmethod
    def test():
        c = Customer({"email": "john@doe.com", "nom": "John Doe", "gender": "male"})

    # Model Logic #

    def sizeConstraints(self, value):
        if value < 130:
            return 130
        elif value > 215:
            return 215
        else:
            return value

    def genderChange(self, before, after):
        print before, after
        return after

    @api.depends('gender')
    def manCompute(self):
        if self.gender is 'male':
            print "MAN", True
            return True
        else:
            print "MAN", False
            return False

    @api.depends('birthday')
    def ageCompute(self):
        return 35

    # End Model's logic #
