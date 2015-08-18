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

from flask import current_app


# TODO pour model dynamique stocker nom Model, nom class, list heritier, nom parent, numéroe sequence
class Context(object):
    _models = dict()

    @classmethod
    def add(cls, tenant, name, obj):
        """ Add models class to a dict by tenant """
        if tenant not in cls._models:
            cls._models[tenant] = dict()
        cls._models[tenant][name] = obj

    @classmethod
    def reset(cls, tenant):
        cls._models.pop(tenant, None)

    def test(self):
        print self._models

    def __getattr__(self, name):
        return self._models[current_app.tenant][name]


model = Context()
