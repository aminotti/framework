from lib.logger import info
from app import api
from app.controller import Controller


def test(self):
    info("Test instance method, instance '{}' : OK!".format(self))


@classmethod
def test1(cls):
    info("Test classmethod, class '{}' : OK!".format(cls))


@staticmethod
def test2():
    info("Test staticmethod : OK!")


# onchange event
def priceChange(self, before, after):
    info("Updating price : before '{}', after '{}'.".format(before, after))
    return after


# Compute field
@api.depends('paypalCode')
def capitaleCompute(self):
    info("Compute Field capitale.")
    if self.paypalCode is 'FR':
        return "Paris"
    else:
        return "NC"


# Constraint
def nameConstraints(self, value):
    info("Processing name constraints.")
    return value.capitalize()
