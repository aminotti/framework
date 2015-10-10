from flask import current_app
from app.controller import Controller
from app.context import models


ctl = Controller()


@ctl.route('/')
def hello():
    return "Hello World {}!".format(current_app.tenant)


@ctl.route('/<int:code>/')
def name(code):
    return "Hello World code {}!".format(code)


@ctl.route('/test/')
def test():
    print models.Country.whoami()
    print models.get('Country').whoami()

    models.Country.test1()
    models.Country.test2()

    c1 = models.Country(name="france", price=7.99, paypalCode="FR")
    print c1.name
    print c1.price
    print c1.paypalCode
    print c1.ville

    c2 = models.Country({"name": "germany", "price": 8.99})
    print c2.name
    print c2.price
    c2.test()
    c2.paypalCode = "DE"
    print c2.ville

    return "Testing..."
