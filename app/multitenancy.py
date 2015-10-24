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
import json
from werkzeug.exceptions import NotFound, HTTPException, default_exceptions
from flask import Flask, request
from flask import jsonify
from lib.exceptions import CoreException
from .config import conf
from lib.logger import debug, error, info
from .module import SmartManagement

# Defaults routes must be last import
from .defaults_routes import ctl as ctl_defaults_routes


class WSGIApp(Flask):
    def __init__(self, import_name):
        super(WSGIApp, self).__init__(import_name)

        # Format internal error message to JSON
        if conf.debug_level in [0, 1]:
            for code in default_exceptions.iterkeys():
                self.error_handler_spec[None][code] = self.__make_json_error

        # Set headers for all response
        self.after_request(self.__setHeaders)

    # Return error information if debug_level = 1,
    # if 0 return HTTP code 500 and generic HTTP message
    def __make_json_error(self, ex):
        if isinstance(ex, CoreException):
            response = jsonify(msg=ex.infos)
            if conf.debug_level != 1:
                response.data = json.dumps({"msg": ex.message})
        else:
            response = jsonify(msg=str(ex))
            if conf.debug_level != 1:
                response.data = json.dumps({"msg": "Internal Server Error"})

        response.headers["Content-type"] = "application/json;charset=utf-8"
        response.headers.add('Server', conf.server_name)
        response.status_code = (500
                                if isinstance(ex, HTTPException)
                                else ex.code)
        return response

    def __setHeaders(self, response):
        response.headers.add('Server', conf.server_name)
        # Enable Cross-Origin Resource Sharing (CORS) for all domain
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response


class AppDispatcher(object):
    """ Create one flask app per tenant """

    regex = re.compile(conf.tenancy)

    def __init__(self):
        self.lock = Lock()
        self.instances = {}

    def _get_application(self, host):
        if conf.multi_tenancy:
            host = host.split(':')[0]
            tenant = ''.join(self.regex.findall(host))

            if not tenant:
                error("Regular expression ' {}' don't match with '{}', please check 'tenancy' option".format(conf.tenancy, host))
                return NotFound()

            debug("Tenancy's prefix for host '{}' : '{}'.".format(host, tenant))
        else:
            debug("Multi-tenancy is disabled.")
            tenant = "yameo"

        with self.lock:
            app = self.instances.get(tenant)
            if app is None:
                app = self._create_app(tenant)
                self.instances[tenant] = app
            return app

    def __call__(self, environ, start_response):
        app = self._get_application(environ['HTTP_HOST'])
        return app(environ, start_response)

    def _create_app(self, tenant):
        if conf.auto_create_db:
            # TODO Creation auto de db (et des different backend pour ce tenancy) et populate si un param de conf est a true pour auto create tenancy et ajout d'une route special pour faire ca.
            pass

        app = WSGIApp(__name__)
        app.debug = conf.debug_level > 1
        app.tenant = tenant

        debug("Building app for tenant '{}'.".format(app.tenant))

        ctl_defaults_routes.buildRoutes(app)
        SmartManagement.loadModules(app)

        return app

application = AppDispatcher()
