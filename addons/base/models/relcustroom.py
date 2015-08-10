from lib.orm import *
from app import HTTPMethod
from config import conf


class RelCustRoom(HTTPMethod, SQLRelationship):
    uri = conf.sample_moduleDb_uri

    customer = ForeignKey('Customer', identifier=True)
    room = ForeignKey('Room', identifier=True)
    reservation = DateField()
    logo = BinaryField(notNone=False)
