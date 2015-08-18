from flask import current_app
from app.controller import Controller
from app.context import model


ctl = Controller()


@ctl.route('/')
def Hello():
    model.Truc.getLol()
    return "Hello World {}!".format(current_app.tenant)
