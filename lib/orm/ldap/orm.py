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

from ..base import Mapper


class ORM(Mapper):
    @classmethod
    def setupConnection(cls, uri, tenant):
        return dict()

    @staticmethod
    def whoami():
        return "LDAP"

    @classmethod
    def update(cls, domain, ressource):
        # Parent method check data and return secured data to save
        data2save = super(ORM, cls).update(domain, data)

    def write(self):
        # Parent method test if require fields are set
        super(ORM, self).write()
