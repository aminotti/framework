from flask import current_app
from app.controller import Controller
from app.context import model


ctl = Controller()


@ctl.route('/')
def Hello():
    print model.Customer.whoami()
    c = model.Customer({"email": "john@doe.com", "nom": "John Doe", "gender": "male"})
    print "#1", c.gender
    c.gender = 'femele'
    c.cm = '45'
    # print c.__dict__
    # print c.__class__.__dict__
    print "#2", c.email
    print "#3", c.gender
    print "#4", c.cm
    return "Hello World {}!".format(current_app.tenant)
