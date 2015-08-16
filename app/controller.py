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


class Controller(object):

    def __init__(self):
        self.routes = list()

    def route(self, rule, **options):
        def decorator(f):
            endpoint = options.pop('endpoint', None)
            data = dict()
            data['rule'] = rule
            data['endpoint'] = endpoint
            data['function'] = f
            data['options'] = options
            self.routes.append(data)
            return f
        return decorator

    def buildRoutes(self, app):
        prefix = self.__class__.__module__
        for data in self.routes:
            data['function'].__name__ = prefix + "_" + data['function'].__name__
            app.add_url_rule(data['rule'], data['endpoint'], data['function'], **data['options'])
