from flask import current_app
from app.controller import Controller
from app.context import models


ctl = Controller()


@ctl.route('/<int:code>/')
def name(code):
    book = models.Booking.get(code)
    if book:
        print "###", book.name
        book.unlink()
    return "Hello World code {}, app {}!".format(code, current_app.tenant)


@ctl.route('/test2/')
def test2():
    return str(models.Hooks._hookable)


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
