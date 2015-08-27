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


from ..exceptions import *
from .fields import Field, Index


class MapperMetaCls(type):
    def __new__(mcs, name, bases, d):
        for parent in bases:
            if parent.__base__.__name__ is 'Mapper':
                d['_columns'] = [field for field in d if isinstance(d[field], Field)]
                d['_Identifiers'] = [field for field in d['_columns'] if d[field].identifier]
                d['_indexes'] = [index for index in d if isinstance(d[index], Index)]

                for field in d['_columns']:
                    d['_' + field] = d.pop(field)

                # TODO gerer relations
                # one2many[name] = list()

        return type.__new__(mcs, name, bases, d)


class HTTPMethods(object):
    pass


class Mapper(HTTPMethods):
    """ Base class for ORM's drivers implementation. """

    __metaclass__ = MapperMetaCls

    # TODO Add internal fields (on backend herited class??)
    # create_date
    # create_uid
    # update_date
    # update_uid
    # active
    # state ('readonly', 'required', 'invisible')

    def __init__(self, *args, **kwargs):
        # Load defaults values to fields
        self._fields = dict()
        for fieldname in self._columns:
            field = getattr(self, '_' + fieldname)
            self._fields[fieldname] = field.default

        for dictionary in args:
            for key in dictionary:
                if key not in self._columns:
                    raise Core400Exception("Bad attribute : '{}'".format(key))
                setattr(self, key, dictionary[key])

        for key in kwargs:
            if key not in self._columns:
                raise Core400Exception("Bad attribute : '{}'".format(key))
            setattr(self, key, kwargs[key])

    def __setattr__(self, name, value):
        if name in self._columns:
            field = getattr(self, '_' + name)
            # TODO Check ACL RW allowed
            # Syntax/type checks
            field.check(value)
            # TODO appeler les differentes method onChange et compute
            # Applying constraints
            if field.constraints:
                value = field.constraints(value)
            # Set to default value if value is None
            if not value and field.default:
                value = field.default
            # Don"t set to None require's fields
            if not field.require or value:
                self._fields[name] = value
        else:
            object.__setattr__(self, name, value)

    def __getattr__(self, name):
        if name in self._columns:
            # TODO Check ACL RO or RW allowed
            return self._fields[name]
        else:
            return object.__getattr__(self, name)

    @staticmethod
    def whoami():
        """ Return the name of the driver use.

        :return str: The name of the backend driver.
        """
        raise NotImplementedError

    """
    def __copy__(self):
        newone = type(self)()
        # TODO implement en retirant les champs mis a copy=False
        newone.__dict__.update(self.__dict__)
        return newone
    """

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
        ressource = cls(data)
        data2save = [ressource[k] for k in data.keys()]

    @classmethod
    def delete(cls, domain):
        """ Delete several records base on the search domain. """
        raise NotImplementedError

    def write(self):
        """ Create or update the ressource. """
        # TODO renvoyer l'id pour une creation!!
        for fieldname in self._columns:
            field = getattr(self, '_' + fieldname)
            if field.require and not self._fields[fieldname]:
                raise Core400Exception("Attribut '{}' is required".format(fieldname))

    def unlink(self):
        """ Delete the ressource. """
        raise NotImplementedError
