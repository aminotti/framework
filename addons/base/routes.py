from flask import current_app
from app.controller import Controller
from app.context import model


ctl = Controller()


@ctl.route('/')
def Hello():
    print model.get('Customer').whoami()
    c = model.Customer({"nom": "John Doe", "gender": "male"})
    print "#1", c.gender
    c.gender = 'femele'
    c.cm = 45
    c.email = 'john@doe.com'
    c.email = None
    print "#2", c.email
    print "#3", c.gender
    print "#4", c.cm
    print "#5", c.age
    return "Hello World {}!".format(current_app.tenant)
