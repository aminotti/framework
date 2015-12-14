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

import sys
import os
import yaml
from lib.exceptions import *
from lib.logger import error


class Conf(object):
    _options = dict()

    def __init__(self):
        self._options = yaml.load(open('config.yaml'))
        self._initCliArgs()
        self._initENVArgs()

    def __getattr__(self, name):
        if name in self._options and 'value' in self._options[name]:
            return self._options[name]['value']
        else:
            raise Core500Exception("Error on option : '{}'".format(name))

    def _initCliArgs(self):
        for arg in sys.argv:
            if arg.startswith('--'):
                data = arg.split('=')
                name = self.__cli2OptName(data[0])

                if name:
                    if len(data) > 1:
                        self._options[name]['value'] = self.__str2OptType(data[1], self._options[name]['type'])
                    else:
                        self._options[name]['value'] = True

    def _initENVArgs(self):
        """ Override config file with ENV and command line arguement """
        for name in self._options.keys():
            value = os.getenv(name.upper())
            if value:
                self._options[name]['value'] = self.__str2OptType(value, self._options[name]['type'])

    def __cli2OptName(self, name):
        optname = name[2:].lower().replace('-', '_')
        if optname not in self._options:
            error("Invalid CLI arguement : '{}'".format(name))
            return None
        else:
            return optname

    def __str2OptType(self, value, opttype):
        if opttype == 'integer':
            return int(value)
        elif opttype == 'boolean':
            if value is '0' or value.lower() == 'false':
                return False
            else:
                return True
        else:
            return value


conf = Conf()

# Add modules directories to python path
conf.module_path = conf.module_path.split(',')
sys.path += conf.module_path
