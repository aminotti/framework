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
#
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
import inspect
import glob
from sets import Set
import yaml
from werkzeug.routing import Map, Rule

from lib.logger import error, debug
from lib.exceptions import *
from app.config import conf
from app.context import models
from app import controller
from lib.orm import base


def loadMetadata():
    # requires values
    info_require = ['name', 'description', 'author', 'email', 'website', 'git']

    # Import every module's metadata module
    modules_infos = dict()

    modules = list()
    for mod_path in conf.module_path:
        modules += [{os.path.join(mod_path, f, 'metadata.yaml'): f} for f in os.listdir(mod_path) if os.path.isfile(os.path.join(mod_path, f, 'metadata.yaml'))]

    seen = set()
    for module in modules:
        name = module.values()[0]
        if name in seen:
            raise Core500Exception("Duplicated module '{}'".format(name))
        seen.add(name)

        # metadata = __import__(module, globals(), locals(), ['infos'], -1)
        metadata = yaml.load(open(module.keys()[0]))
        for info in info_require:
            if info not in metadata:
                raise Core500Exception("'%s' field is required in %s" % (info, module))

        # Set default values
        metadata.setdefault('icon', 'default.png')
        metadata.setdefault('version', '1.0')
        metadata.setdefault('license', "AGPL-3")
        metadata.setdefault('auto-install', False)
        metadata.setdefault('auto-upgrade', False)
        metadata.setdefault('auto-remove', False)

        # Check if both auto-install and auto-remove are set to True
        if metadata['auto-install'] and metadata['auto-remove']:
                raise Core500Exception("Both 'auto-install' and 'auto-remove' can't be set to True for module {}.".format(module.split('.')[0]))

        modules_infos[module.values()[0]] = metadata

    return modules_infos


class SmartManagement(object):
    """ This class manage module : install, upgrade, remove and the load process on tenant app creation. """

    metadata = loadMetadata()
    """  To get a list sorted by module name : ``sorted(SmartManagement.metadata.values(), key=lambda row: row['name'])``  """

    @classmethod
    def loadModules(cls, app):
        """ Call this method to load module on app start.
            This method proceed auto-install, auto-upgrade and auto-remove before loading modules.
        """
        cls.local = cls._loadLocalModuleList()
        cls.installed = cls._loadInstalledModuleList(app.tenant)
        cls._autoRemove(Set(cls.local['remove']) & Set(cls.installed))
        cls._autoUpgrade(Set(cls.local['upgrade']) & Set(cls.installed))
        cls._autoInstall(Set(cls.local['install']) - Set(cls.installed))
        cls._saveInstalledModuleList(cls.installed, app.tenant)
        cls._importAll(app)

    @classmethod
    def install(cls, module, app):
        """ Call this method when user click on install button.

        :param str module: Module identifier.
        """
        # cls.installed = cls._loadInstalledModuleList(app.tenant)
        # cls._autoInstall([module])
        # cls._saveInstalledModuleList(cls.installed, app.tenant)
        cls._reset_app(app)

    @classmethod
    def ugrade(cls, module, app):
        """ Call this method when user click on upgrade button.

        :param str module: Module identifier.
        """
        cls._autoUpgrade([module])
        cls._reset_app(app)

    @classmethod
    def remove(cls, module, app):
        """ Call this method when user click on remove button.

        :param str module: Module identifier.
        """
        cls.installed = cls._loadInstalledModuleList(app.tenant)
        cls._autoRemove([module])
        cls._saveInstalledModuleList(cls.installed, app.tenant)
        cls._reset_app(app)

    @classmethod
    def _loadLocalModuleList(cls):
        local = dict()
        local['install'] = list()
        local['upgrade'] = list()
        local['remove'] = list()
        for key, val in cls.metadata.items():
            if val['auto-install']:
                local['install'].append(key)
            if val['auto-upgrade']:
                local['upgrade'].append(key)
            if val['auto-remove']:
                local['remove'].append(key)
        return local

    @classmethod
    def _loadInstalledModuleList(cls, tenant):
        # TODO init installed from DB
        installed = list()
        # installed.append('base')
        installed.append('beta_test')
        if tenant == 'meezio':
            installed.append('base_perso')
        installed.append('mod_test')
        return installed

    @classmethod
    def _autoInstall(cls, modules):
        for module in modules:
            # TODO call onInstall() from all module's model
            # TODO gerer install des dependances python qd elle sont pas présente
            # TODO gerer dependance d'autre module => on ajout tous les modules dont il depend (doit etre recursif)
            cls.installed.append(module)

    @classmethod
    def _autoUpgrade(cls, modules):
        for module in modules:
            # TODO call onUpgrade() from all module's model
            pass

    @classmethod
    def _autoRemove(cls, modules):
        for module in modules:
            # TODO call onRemove() from all module's model
            # TODO gerer dependance d'autre module => on supprime tous les modules qui depende de lui (doit etre recursif)
            cls.installed.remove(module)

    @classmethod
    def _saveInstalledModuleList(cls, installed, tenant):
        # TODO save installed to DB
        pass

    @classmethod
    def _importAll(cls, app):
        debug("Addons to load for tenant '{}' : {}.".format(app.tenant, cls.installed))
        for mod in cls.installed:
            cls._loadModule(mod, app)

        # Import registered YAML model for current tenant/app
        models.buildRegistered(app)

    @classmethod
    def _loadModule(cls, module, app):
        mod = __import__(module, globals(), locals(), ['*'], -1)
        modelpath = os.path.join(os.path.dirname(mod.__file__), 'models')

        for attr in dir(mod):
            obj = getattr(mod, attr, None)
            # Load standalone routes for current tenant/app
            if isinstance(obj, controller.Controller):
                obj.buildRoutes(app)
            # Load python class models for current tenant/app
            elif inspect.isclass(obj) and issubclass(obj, base.Mapper):
                models.add(app.tenant, attr, obj)

        # Register YAML models for current tenant/app
        if os.path.isdir(modelpath):
            for modelfile in glob.glob(os.path.join(modelpath, '*.yaml')):
                models.register(app.tenant, modelfile)

        # TODO Import view (xml) for current tenant/app
        # TODO Import data (json, yaml, csv) for current tenant/app
        # TODO Import workflow (xml ? yaml?) for current tenant/app

    @classmethod
    def _reset_app(cls, app):
        # TODO si docker avec plusieurs instance de lancé, killer les autres instances
        # TODO Remove views
        # TODO Remove datas
        # TODO Remove workflows

        # Remove Models
        models.reset(app.tenant)
        # Reset to default Flask route
        app.url_map = Map([Rule('/static/<filename>', methods=['HEAD', 'OPTIONS', 'GET'], endpoint='static')])
        cls._importAll(app)
