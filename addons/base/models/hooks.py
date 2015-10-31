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


from app.context import models
from lib.exceptions import *


def ressourceConstraints(self, value):
    ressource = value.lower().capitalize()
    if not models.get(ressource):
        raise Core400Exception("Ressource '{}' doesn't exist.".format(ressource))
    return ressource


def write(self):
    # Test if ressource is hookable before performing normal process
    if models.get(self.ressource)._hookable:
        super(self.__class__, self).write()
    else:
        raise Core400Exception("Ressource '{}' is not hookable.".format(self.ressource))


def update(self, data2save, domain):
    # Test if ressource is hookable before performing normal process
    if models.get(self.ressource)._hookable:
        super(self.__class__, self).update(data2save, domain)
    else:
        raise Core400Exception("Ressource '{}' is not hookable.".format(self.ressource))
