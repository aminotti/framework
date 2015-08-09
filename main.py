#!/usr/bin/env python
# -*-coding:utf-8 -*

from app.multitenancy import application
from werkzeug.serving import run_simple
from app.config import conf

if __name__ == '__main__':
    debug = conf.debug_level > 1
    run_simple('localhost', 5000, application, use_reloader=debug, use_debugger=debug, use_evalex=debug)
