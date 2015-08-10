from lib.orm import *
from app import HTTPMethod


class Room(HTTPMethod, SQLTable):
    batiment = IntField(size=2, zerofill=True, identifier=True, unsigned=True, default=1)
    number = IntField(size=3, zerofill=True, identifier=True, unsigned=True)
    name = StringField(fieldName='room_name', length=150)
    idx = Index('name')
    contrat = BinaryField(notNone=False, backendFS=False)
