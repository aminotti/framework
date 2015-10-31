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

import datetime
import json
from app.context import models
import lib.hook
from lib.exceptions import *


class HookManager(object):

    @classmethod
    def exeCreate(cls, ressource):
        hooks = models.Hooks.search([('ressource', '=', ressource.__class__.__name__), ('action', '=', 'create'), ('active', '=', '1')])
        for hook in hooks:
            driver = getattr(lib.hook, hook.type)
            try:
                settings = json.loads(hook.settings)
            except ValueError:
                raise Core400Exception("Settings must be formated in valid JSON")
            msg = driver.runCreate(hook.ressource, settings, ressource._fields)
            hook.exec_date = datetime.datetime.now()
            hook.exec_message = msg
            hook.write()

    @classmethod
    def exeUpdate(cls, ressource, data2save, identifiers):
        hooks = models.Hooks.search([('ressource', '=', ressource.__class__.__name__), ('action', '=', 'update'), ('active', '=', '1')])
        for hook in hooks:
            driver = getattr(lib.hook, hook.type)
            data = {key: ressource._fields[key] for key in data2save}
            try:
                settings = json.loads(hook.settings)
            except ValueError:
                raise Core400Exception("Settings must be formated in valid JSON")
            msg = driver.runUpdate(hook.ressource, settings, identifiers, data)
            hook.exec_date = datetime.datetime.now()
            hook.exec_message = msg
            hook.write()

    @classmethod
    def exeDelete(cls, ressource_cls, identifiers):
        hooks = models.Hooks.search([('ressource', '=', ressource_cls.__name__), ('action', '=', 'delete'), ('active', '=', '1')])
        for hook in hooks:
            driver = getattr(lib.hook, hook.type)
            try:
                settings = json.loads(hook.settings)
            except ValueError:
                raise Core400Exception("Settings must be formated in valid JSON")
            msg = driver.runDelete(hook.ressource, settings, identifiers)
            hook.exec_date = datetime.datetime.now()
            hook.exec_message = msg
            hook.write()
