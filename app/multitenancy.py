# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (C) 2014-2015 Anthony Minotti <anthony@minotti.cool>.
#
#
# This file is part of Yameo framework.
#
# Yameo framework is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Yameo framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Yameo framework.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import re
from threading import Lock
from flask import Flask, request
from werkzeug.exceptions import NotFound
from .config import conf
from lib.logger import debug, error, info
from .module import SmartManagement


class AppDispatcher(object):
    """ Create one flask app per tenant """

    regex = re.compile(conf.tenancy)

    def __init__(self):
        self.lock = Lock()
        self.instances = {}

    def _get_application(self, host):
        host = host.split(':')[0]
        tenant = ''.join(self.regex.findall(host))

        if not tenant:
            error("Regular expression ' {}' don't match with '{}', please check 'tenancy' option".format(conf.tenancy, host))
            return NotFound()

        debug("Tenancy's prefix for host '{}' : '{}'.".format(host, tenant))

        with self.lock:
            app = self.instances.get(tenant)
            if app is None:
                app = self._create_app(tenant)
                self.instances[tenant] = app
            print id(app)
            return app

    def __call__(self, environ, start_response):
        app = self._get_application(environ['HTTP_HOST'])
        return app(environ, start_response)

    def _create_app(self, tenant):
        if conf.auto_create_db:
            # TODO Creation auto de db et populate
            pass

        app = Flask(__name__)
        app.tenant = tenant

        debug("Building app for tenant '{}'.".format(app.tenant))

        @app.route('/install/<module>')
        def install(module):
            SmartManagement.install(module, app)
            return "Install ok!!"

        SmartManagement.loadModules(app)

        return app

application = AppDispatcher()
