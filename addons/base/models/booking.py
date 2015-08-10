from lib.orm import *
from app import HTTPMethod
from config import conf


class Booking(HTTPMethod, SQLView):
    uri = conf.sample_moduleDb_uri

    nom = StringField(fieldName='fullname')
    batiment = IntField()
    email = email = EmailField()
    reservation = DateField()
    name = StringField(fieldName='room_name')
