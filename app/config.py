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


class Conf(object):
    options = dict()

    def __init__(self):
        self._initOptions()
        self._loadConfig()

    def _initOptions(self):
        for arg in sys.argv:
            if arg.startswith('--'):
                data = arg.split('=')
                if len(data) > 1:
                    options[data[0]] = data[1]
                else:
                    options[data[0]] = True

    def _loadConfig(self):
        # Global conf
        cf = yaml.load(open('config.yaml'))
        for k, v in cf.items():
            if type(v) is dict:
                for n, d in v.items():
                    setattr(self, k + n.capitalize(), self._overrideConf(k + n.capitalize(), d))
            else:
                setattr(self, k, self._overrideConf(k, v))

        # Modules conf
        """
        configs = [{'name': f, 'path': 'modules/%s/config.yaml' % f} for f in os.listdir('modules') if os.path.isfile('modules/%s/config.yaml' % f)]
        for config in configs:
            data = yaml.load(open(config['path']))
            for k, v in data.items():
                name = config['name'] + k.capitalize()
                setattr(self, name, self._overrideConf(name, v))
        """

    def _overrideConf(self, key, value):
        """ Override config file with ENV and command line arguement """
        return self.options.get('--' + key.lower().replace('_', '-'), os.getenv(key.upper(), value))

conf = Conf()

# Add modules directories to python path
conf.module_path = conf.module_path.split(',')
sys.path += conf.module_path
