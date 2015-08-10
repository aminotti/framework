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
from sets import Set
from lib.logger import error
from lib.exceptions import *
from app.config import conf


def loadMetadata():
    # requires values
    info_require = ['name', 'description', 'author', 'email', 'website', 'git']

    # Import every module's metadata module
    modules_infos = dict()

    modules = list()
    for mod_path in conf.module_path:
        modules += ['%s.metadata' % f for f in os.listdir(mod_path) if os.path.isfile(os.path.join(mod_path, f, 'metadata.py'))]

    # Remove duplicated modules
    modules = list(set(modules))

    for module in modules:
        metadata = __import__(module, globals(), locals(), ['*'], -1)
        for info in info_require:
            if info not in metadata.infos:
                raise Core500Exception("'%s' field is required in %s" % (info, module))

        # Set default values
        metadata.infos.setdefault('icon', 'default.png')
        metadata.infos.setdefault('version', '1.0')
        metadata.infos.setdefault('license', "AGPL-3")
        metadata.infos.setdefault('auto-install', False)
        metadata.infos.setdefault('auto-upgrade', False)
        metadata.infos.setdefault('auto-remove', False)

        # Check if both auto-install and auto-remove are set to True
        if metadata.infos['auto-install'] and metadata.infos['auto-remove']:
                raise Core500Exception("Both 'auto-install' and 'auto-remove' can't be set to True for module {}.".format(module.split('.')[0]))

        modules_infos[module.split('.')[0]] = metadata.infos

    return modules_infos


class SmartManagement(object):
    """ This class manage module : install, upgrade, remove and the load process on tenant app creation. """

    metadata = loadMetadata()
    """  To get a list sorted by module name : ``sorted(SmartManagement.metadata.values(), key=lambda row: row['name'])``  """

    @classmethod
    def loadModules(cls, tenant):
        """ Call this method to load module on app start.
            This method proceed auto-install, auto-upgrade and auto-remove before loading modules.
        """
        cls.local = cls._loadLocalModuleList()
        cls.installed = cls._loadInstalledModuleList(tenant)
        cls._autoRemove(Set(cls.local['remove']) & Set(cls.installed))
        cls._autoUpgrade(Set(cls.local['upgrade']) & Set(cls.installed))
        cls._autoInstall(Set(cls.local['install']) - Set(cls.installed))
        cls._saveInstalledModuleList(cls.installed, tenant)
        cls._importAll(tenant)

    @classmethod
    def install(cls, module, request, tenant):
        """ Call this method when user click on install button.

        :param str module: Module identifier.
        """
        cls.installed = cls._loadInstalledModuleList(tenant)
        cls._autoInstall([module])
        cls._saveInstalledModuleList(cls.installed, tenant)
        cls._shutdown_app(request)

    @classmethod
    def ugrade(cls, module, request):
        """ Call this method when user click on upgrade button.

        :param str module: Module identifier.
        """
        cls._autoUpgrade([module])
        cls._shutdown_app(request)

    @classmethod
    def remove(cls, module, request, tenant):
        """ Call this method when user click on remove button.

        :param str module: Module identifier.
        """
        cls.installed = cls._loadInstalledModuleList(tenant)
        cls._autoRemove([module])
        cls._saveInstalledModuleList(cls.installed, tenant)
        cls._shutdown_app(request)

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
        # TODO search in DB
        installed = list()
        # installed.append('base')
        installed.append('test')
        installed.append('truc')
        installed.append('mod_test')
        return installed

    @classmethod
    def _autoInstall(cls, modules):
        for module in modules:
            print '##### I', module
            # TODO call onInstall() from all module's model
            # TODO gerer install des dependances python qd elle sont pas présente
            # TODO gerer dependance d'autre module => on ajout tous les modules dont il depend (doit etre recursif)
            cls.installed.append(module)

    @classmethod
    def _autoUpgrade(cls, modules):
        for module in modules:
            print '##### U', module
            # TODO call onUpgrade() from all module's model

    @classmethod
    def _autoRemove(cls, modules):
        for module in modules:
            print '##### R', module
            # TODO call onRemove() from all module's model
            # TODO gerer dependance d'autre module => on supprime tous les modules qui depende de lui (doit etre recursif)
            cls.installed.remove(module)

    @classmethod
    def _saveInstalledModuleList(cls, installed, tenant):
        # TODO save installed to DB
        pass

    @classmethod
    def _importAll(cls, tenant):
        # TODO
        print cls.installed, " for " + tenant

    @classmethod
    def loadModule(cls, module):
        pass

    @classmethod
    def _shutdown_app(cls, request):
        # TODO kill app or manual reimport module
        print "######"
        func = request.environ.get('werkzeug.server.shutdown')
        print "######"
        if func is None:
            error("Can't reload app, manual restart needed.")
        else:
            print "$$$$"
            func()
