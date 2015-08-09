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


class Mapper(object):
    """ Base class for ORM's drivers implementation. """

    @classmethod
    def onInstall(cls):
        """ A method excute on module install. """
        pass

    @classmethod
    def onUpgrade(cls):
        """ A method excute on module upgrade. """
        pass

    @classmethod
    def onRemove(cls):
        """ A method excute when removing module. """
        pass

    @classmethod
    def search(cls, domain, fields=None, count=None, offset=None, sort=None):
        """ Searches for records based on the search domain

Model.search(filter, sort_by=None(field or dict of fields {'field': reverse(default False)}), count=, offset=0) : return list of matching record

        :param domain: Search filter.
        :param list fields: List of fields to return.
        :param int count: number of ressources to return.
        :param int offset: The offset of the first ressource to return.
        :param dict or srt sort: The fields use to sort the result. To use several field or inverse order use a dict like ``{'fieldname': True}``
        :return: A ressource or a list of ressources.
        """
        raise NotImplementedError

    @classmethod
    def update(cls, domain, data):
        """ Update several records base on the search domain.

        :param domain: search filter
        :param dict data: data use to update fields.
        """
        raise NotImplementedError

    @classmethod
    def delete(cls, domain):
        """ Delete several records base on the search domain. """
        raise NotImplementedError

    def write(self):
        """ Create or update the ressource. """
        raise NotImplementedError

    def unlink(self):
        """ Delete the ressource. """
        raise NotImplementedError
