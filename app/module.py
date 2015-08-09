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

from sets import Set


class SmartManagement(object):
    """ This class manage module : install, upgrade, remove and the load process on tenant app creation. """

    @classmethod
    def loadModule(cls):
        """ Call this method to load module on app start. """
        local = cls._loadLocalModuleList()
        installed = cls._loadInstalledModuleList()
        cls._autoRemove(Set(local['remove']) & Set(installed))
        cls._autoUpgrade(Set(local['upgrade']) & Set(installed))
        cls._autoInstall(Set(local['install']) - Set(installed))
        cls._importAll()

    @classmethod
    def install(cls, module):
        """ Call this method when user click on install button.

        :param str module: Module identifier.
        """
        cls._autoInstall([module])
        # TODO kill app

    @classmethod
    def ugrade(cls, module):
        """ Call this method when user click on upgrade button.

        :param str module: Module identifier.
        """
        cls._autoUpgrade([module])
        # TODO kill app

    @classmethod
    def remove(cls, module):
        """ Call this method when user click on remove button.

        :param str module: Module identifier.
        """
        cls._autoRemove([module])
        # TODO kill app

    @classmethod
    def _loadLocalModuleList(cls):
        # TODO look in addons directories
        # TODO Raise exception si auto-install & auto-remove
        local = dict()
        local['install'] = ['test', 'new']
        local['upgrade'] = ['test', 'max']
        local['remove'] = ['truc', 'plot']
        return local

    @classmethod
    def _loadInstalledModuleList(cls):
        # TODO search in DB
        installed = list()
        installed.append('base')
        installed.append('test')
        installed.append('truc')
        return installed

    @classmethod
    def _autoInstall(cls, modules):
        for module in modules:
            print '##### I', module
            # TODO call onInstall() from all module's model
            # TODO gerer dependance d'autre module => on ajout tous les modules dont il depend (doit etre recursif)
        # TODO cls.installed et store db

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
        # TODO cls.installed et store db

    @classmethod
    def _importAll(cls):
        # TODO
        pass
