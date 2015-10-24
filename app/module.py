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
from lib.orm.pool import Pool


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
        metadata.setdefault('auto-remove', False)
        metadata.setdefault('depends', list())

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
            This method proceed auto-install and auto-remove before loading modules.
        """
        # Modules present on file system
        cls.local = cls._loadLocalModuleList()
        # Modules saved in DB as installed
        cls.installed = cls._loadInstalledModuleList(app.tenant)
        # Module to install
        cls.toInstall = list(Set(cls.local['install']) - Set(cls.installed))

        # Load installed module + module to install - module to Remove
        cls._autoRemove(Set(cls.local['remove']) & Set(cls.installed))
        cls._beforeAutoInstall(cls.toInstall)
        cls._importAll(app)
        cls._afterAutoInstall(app.tenant, cls.toInstall)

        cls._saveInstalledModuleList(cls.installed, app.tenant)

    @classmethod
    def install(cls, module, app):
        """ Call this method when user click on install button.

        :param str module: Module identifier.
        """
        # TODO implementer install module avec ajout de route
        # cls.installed = cls._loadInstalledModuleList(app.tenant)
        # cls._autoInstall([module])
        # cls._saveInstalledModuleList(cls.installed, app.tenant)
        cls._reset_app(app)

    @classmethod
    def ugrade(cls, module, app):
        """ Call this method when user click on upgrade button.

        :param str module: Module identifier.
        """
        # TODO ajout de route
        cls._reset_app(app)

    @classmethod
    def remove(cls, module, app):
        """ Call this method when user click on remove button.

        :param str module: Module identifier.
        """
        # TODO implementer remove module avec ajout de route
        # cls.installed = cls._loadInstalledModuleList(app.tenant)
        # cls._autoRemove([module])
        # cls._saveInstalledModuleList(cls.installed, app.tenant)
        cls._reset_app(app)

    @classmethod
    def _loadLocalModuleList(cls):
        local = dict()
        local['install'] = list()
        local['remove'] = list()
        for key, val in cls.metadata.items():
            if val['auto-install']:
                local['install'].append(key)
            if val['auto-remove']:
                local['remove'].append(key)
        return local

    @classmethod
    def _loadInstalledModuleList(cls, tenant):
        installed = list()

        # TODO remplacer tout le bloc pas chargement depuis DB des module deja installé pour ce tenant
        # installed.append('base')
        installed.append('beta_test')
        if tenant == 'meezio':
            installed.append('base_perso')
        installed.append('mod_test')

        return installed

    @classmethod
    def _beforeAutoInstall(cls, modules):
        for module in modules:
            # TODO gerer install des dependances python qd elle sont pas présente
            # TODO gerer dependance d'autre module => on ajout tous les modules dont il depend (doit etre recursif) à cls.installed
            cls.installed.append(module)

    @classmethod
    def _afterAutoInstall(cls, tenant, modules):
        for module in modules:
            for mod in models.modules[tenant][module]:
                models.get(mod, tenant).onInstall()
            # TODO import DATA

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
        Pool.build(conf.max_pool_size)

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
                models.register(app.tenant, modelfile, module)

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
        # TODO reimporter defaults routes
        # from .defaults_routes import ctl as ctl_defaults_routes
        # ctl_defaults_routes.buildRoutes(app)

        cls._importAll(app)
