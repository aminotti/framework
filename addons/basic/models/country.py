from app import api
from app.controller import Controller


def test(self):
    print "## test instance OK!", self


@classmethod
def test1(cls):
    print "## test classmethod OK!", cls


@staticmethod
def test2():
    print "## test staticmethod OK!"


# onchange event
def priceChange(self, before, after):
    print "Updating price", before, after
    return after


# Compute field
@api.depends('paypalCode')
def villeCompute(self):
    print "Compute Field"
    if self.paypalCode is 'FR':
        return "Paris"
    else:
        return "NC"


# Constraint
def nameConstraints(self, value):
    print "Call on writting data."
    return value.capitalize()
