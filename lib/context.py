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

import os
import types
import yaml
import imp
from flask import current_app
from .model import Builder
from .model import default_routes, default_post_routes
from lib.logger import debug
from lib.orm.fields import *


class Context(object):
    _models = dict()
    _regiteredModels = dict()
    modules = dict()

    @classmethod
    def register(cls, tenant, yamlfile, modname):
        """ Register all YAML model's file for later load. """
        """ Get data from <ressource>.yaml and <ressource>.py and store them in _regiteredModels[<tenant>][<ressource>] list. """
        # Load model's function from <ressource>.py
        functions = dict()
        root, ext = os.path.splitext(yamlfile)
        path, name = os.path.split(root)
        module = root + '.py'
        if os.path.isfile(module):
            mod = imp.load_source('{}_{}'.format(tenant, name), module)
            for attr in dir(mod):
                fct = getattr(mod, attr, None)
                # print type(fct)
                if type(fct) in [types.FunctionType, classmethod, staticmethod]:
                    functions[attr] = fct

        modelInfos = yaml.load(open(yamlfile))
        name = modelInfos['name']
        del modelInfos['name']
        modelInfos.setdefault('sequence', 1)
        modelInfos['functions'] = functions

        if tenant not in cls._regiteredModels:
            cls._regiteredModels[tenant] = dict()
            cls.modules[tenant] = dict()

        if modname not in cls.modules[tenant]:
            cls.modules[tenant][modname] = list()

        cls.modules[tenant][modname].append(name)

        if name not in cls._regiteredModels[tenant]:
            cls._regiteredModels[tenant][name] = list()

        cls._regiteredModels[tenant][name].append(modelInfos)

    @classmethod
    def buildRegistered(cls, app):
        tenant = app.tenant
        # TODO checker champs requis présent dans yaml et bon type associé
        if tenant in cls._regiteredModels:
            # Sort by sequence
            for key, val in cls._regiteredModels[tenant].items():
                # Sort data from yaml file
                cls._regiteredModels[tenant][key] = sorted(val, key=lambda row: row['sequence'])
                # append data from DB
                # TODO #200 cls._regiteredModels[tenant][key].append(<data from DB for this model/ressource>)

            # Load models by tenant
            models = dict()
            for name, data in cls._regiteredModels[tenant].items():
                n, b, d, f = Builder.get(name, data, tenant)
                models[n] = [n, b, d, f]

            for name, data in models.items():
                dico = cls._mixeWithParent(data, models)
                dico.update(data[2])

                with app.app_context():
                    obj = type(data[0], data[1], dico)

                    # Add defaults routes
                    identifiers = list()
                    for arg in obj._identifiers:
                        if isinstance(obj.__dict__['_' + arg + '_field'], IntField):
                            identifiers.append("<int:{}>".format(arg))
                        elif isinstance(obj.__dict__['_' + arg + '_field'], CurrencyField) or isinstance(obj.__dict__['_' + arg + '_field'], DecimalField):
                            identifiers.append("<float:{}>".format(arg))
                        elif isinstance(obj.__dict__['_' + arg + '_field'], UrlField):
                            identifiers.append("<path:{}>".format(arg))
                        else:
                            identifiers.append("<{}>".format(arg))

                    rule = '/{}/{}/'.format(name.lower(), "/".join(identifiers))
                    debug("Adding route : '{}'".format(rule))
                    current_app.add_url_rule(rule, 'default_routes_{}'.format(name), default_routes, methods=['GET', 'PUT', 'PATCH', 'DELETE'])
                    rule = '/{}/'.format(name.lower())
                    debug("Adding route : '{}'".format(rule))
                    current_app.add_url_rule(rule, 'default_post_routes_{}'.format(name), default_post_routes, methods=['GET', 'POST'])

                cls.add(tenant, name, obj)

    @classmethod
    def _mixeWithParent(cls, data, models):
        """ Mixe with parent's fields, indexes and functions """

        dico = dict()

        # If parent define
        if data[2]['_inherit']:
            dico.update(cls._mixeWithParent(models[data[2]['_inherit']], models))

        dico.update(data[3])
        return dico

    @classmethod
    def add(cls, tenant, name, obj):
        """ Add models class to a dict by tenant """
        if tenant not in cls._models:
            cls._models[tenant] = dict()
        cls._models[tenant][name] = obj

    @classmethod
    def reset(cls, tenant):
        cls._models.pop(tenant, None)

    def __getattr__(self, name):
        return self._models[current_app.tenant][name]

    def get(self, name, tenant=None):
        """ Beside attribute access, model can be accessed by name. """
        if tenant:
            return self._models[tenant].get(name)
        else:
            return self._models[current_app.tenant].get(name)
