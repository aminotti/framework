from flask import current_app
from app.controller import Controller


ctl = Controller()


@ctl.route('/')
def Hello():
    return "Hello World {}!".format(current_app.tenant)
