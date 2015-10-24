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

import types
import json
from flask import current_app
from ..exceptions import *
from .fields import Field, Index, IntField, StringField
from ..logger import debug, error
from ..httpmethod import HTTPMethods


class MapperMetaCls(type):
    def __new__(mcs, name, bases, d):
        for parent in bases:
            if parent.__base__.__name__ is 'Mapper':
                d['_columns'] = [field for field in d if isinstance(d[field], Field)]
                d['_identifiers'] = [field for field in d['_columns'] if d[field].identifier]
                d['_indexes'] = [index for index in d if isinstance(d[index], Index)]

                if not d['_identifiers']:
                    ressource = name.lower()
                    idressource = "id{}".format(ressource)
                    debug("Create default ID 'id{0}' for '{0}'.".format(ressource))

                    d['_columns'].append(idressource)
                    d['_identifiers'].append(idressource)
                    d[idressource] = IntField(size=6, zerofill=True, unsigned=True, autoIncrement=True, identifier=True, unique=True)

                # Create index for Field with index attribute set to True
                tmp = dict()
                idx = list()
                for f in d:
                    if isinstance(d[f], Field) and not d[f].identifier and d[f].index:
                        tmp['idx' + f] = Index([f])
                        idx.append('idx' + f)
                d.update(tmp)
                d['_indexes'].extend(idx)

                for field in d['_columns']:
                    d['_' + field + '_field'] = d.pop(field)

                # TODO gerer relations
                # one2many[name] = list()

                if '_cacheable' not in d:
                    d['_cacheable'] = False

                if '_hookable' not in d:
                    d['_hookable'] = True

                d.update(bases[0].setupConnection(d['_uri'], current_app.tenant))

        return type.__new__(mcs, name, bases, d)


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

    # Prepare workflow trigger onchange event
    """
    def __new__(cls, *args, **kwargs):
        for attr, val in cls.__dict__.items():
            if isinstance(val, types.FunctionType):
                Créer un dict du genre {attrdpendant, [metho1, method2, method3, ...]}
                print "******", attr, val, hasattr(val, '_onchange')

        return super(Mapper, cls).__new__(cls, *args, **kwargs)
    """

    def __init__(self, *args, **kwargs):
        self._fields = dict()
        computed = dict()

        for fieldname in self._columns:
            field = getattr(self, '_' + fieldname + '_field')

            # Load defaults values to fields
            self._fields[fieldname] = field.default

            # Prepare computed values
            if field.compute:
                f = getattr(self, field.compute, None)
                if not f:
                    raise Core500Exception("Compute method not found : '{}'".format(field.compute))
                else:
                    computed[fieldname] = f

        for dictionary in args:
            for key in dictionary:
                if key not in self._columns:
                    raise Core400Exception("Bad attribute : '{}'".format(key))
                setattr(self, key, dictionary[key])

        for key in kwargs:
            if key not in self._columns:
                raise Core400Exception("Bad attribute : '{}'".format(key))
            setattr(self, key, kwargs[key])

        # Set computed value here cause can depends of previous attributes setted
        for key, val in computed.items():
            self._fields[key] = val()

    def __setattr__(self, name, value):
        if name in self._columns:
            field = getattr(self, '_' + name + '_field')
            # TODO Check ACL RW allowed
            # Serialize dict to string
            if isinstance(field, StringField) and type(value) is dict:
                value = json.dumps(value, ensure_ascii=False)
            # Syntax/type checks
            field.check(value)
            # TODO trigger workflow event onchange
            # Call On change method
            if field.onchange:
                f = getattr(self, field.onchange, None)
                if not f:
                    raise Core500Exception("On change method not found : '{}'".format(field.onchange))
                value = f(self._fields[name], value)
            # Applying constraints
            if field.constraints:
                f = getattr(self, field.constraints, None)
                if not f:
                    raise Core500Exception("Constraints method not found : '{}'".format(field.constraints))
                value = f(value)
            # Set to default value if value is None
            if not value and field.default:
                value = field.default
            # Don"t set to None require's fields
            if (not field.require or value) and not field.compute:
                field.check(value)
                self._fields[name] = value
        # TODO elif name in self._one2one._columns: (boucler sur self._one2one pour avoir acces aux ._columns)
        else:
            object.__setattr__(self, name, value)

    def __getattr__(self, name):
        if name in self._columns:
            field = getattr(self, '_' + name + '_field')
            # TODO Check ACL RO or RW allowed
            # Perform computed Fields
            if field.compute:
                f = getattr(self, field.compute, None)
                if not f:
                    raise Core500Exception("Compute method not found : '{}'".format(field.compute))
                self._fields[name] = f()
                return self._fields[name]
            else:
                return self._fields[name]
        # TODO elif name in self._one2one._columns: (boucler sur self._one2one pour avoir acces aux ._columns)
        else:
            return object.__getattr__(self, name)

    def setIdFromDomain(self, domain):
        if type(domain) is tuple:
            self._setIdFromDomainTuple(domain)
        elif type(domain) is list:
            self._setIdFromDomainList(domain)
        else:
            raise Core400Exception("Invalid domain for identifiers : {}".format(str(domain)))

    def _setIdFromDomainList(self, domain):
        nbid = 0
        for dom in domain:
            if type(dom) is tuple:
                self._setIdFromDomainTuple(dom)
                nbid += 1
        if nbid < len(self._identifiers):
            raise Core500Exception("All identifiers must be set".format(domain))

    def _setIdFromDomainTuple(self, domain):
        if len(domain) != 3 or domain[0] not in self._identifiers:
            raise Core400Exception("Bad identifier : '{}'".format(domain[0]))
        else:
            setattr(self, domain[0], domain[2])

    @classmethod
    def setupConnection(cls, uri, tenant):
        """ Add connections to pools and set backend specifics attributes. """
        error("setupConnection() method not implemented for {}".format(cls.whoami()))
        raise NotImplementedError

    @classmethod
    def parseURI(cls, uri):
        port = None
        user = None
        password = None
        param = None

        if '://' not in uri:
            raise Core500Exception("Bad syntax : {}".format(uri))
        scheme, rest = uri.split('://', 1)
        if "@" in rest:
            user, rest = rest.split('@', 1)
            if ":" in user:
                user, password = user.split(':', 1)
        if "/" in rest:
            host, param = rest.split('/', 1)
        else:
            host = rest
        if ":" in host:
            host, port = database.split(':', 1)

        return scheme, user, password, host, port, param

    @staticmethod
    def whoami():
        """ Return the name of the driver use.

        :return str: The name of the backend driver.
        """
        error("whoami() method not implemented for this driver")
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
    def get(cls, *identifiers):  # TODO add expend = True pour toucher les relation au lieux de leur id
        """
        Get a ressource by identifiers.

        ;return : A ressource maching the identifiers or None if not found.
        """
        domain = list()
        i = 0

        if len(identifiers) != len(cls._identifiers):
            raise Core500Exception("'{}' : Bad number of identifiers".format(str(identifiers)))

        for identifier in cls._identifiers:
            col = getattr(cls, "_{}_field".format(identifier), None)
            col.check(identifiers[i])
            domain.append((identifier, '=', identifiers[i]))
            i += 1

        ressources = cls.search(domain)
        if ressources:
            return ressources[0]
        else:
            return None

    @classmethod
    def search(cls, domain, fields=None, count=None, offset=None, sort=None):
        """ Searches for records based on the search domain

        :param domain: Search filter.
        :param list fields: List of fields to return.
        :param int count: number of ressources to return.
        :param int offset: The offset of the first ressource to return.
        :param dict or srt sort: The fields use to sort the result. To use several field or inverse order use a dict like ``{'fieldname': True}``
        :return: A ressource or a list of ressources.
        """
        error("search() method not implemented for {}".format(cls.whoami()))
        raise NotImplementedError

    def update(self, data2save, domain):
        """ Update several records base on the search domain.
        Use data store in instance to do sanity and security check.
        Use data2save to select fields to save.

        :param list data2save: name of ressource's fields to save.
        :param domain: search filter.
        """
        error("update() method not implemented for {}".format(cls.whoami()))
        raise NotImplementedError

    @classmethod
    def delete(cls, domain):
        """ Delete several records base on the search domain. """
        error("delete() method not implemented for {}".format(cls.whoami()))
        raise NotImplementedError

    def write(self):
        """
        Create or update the ressource.

        @return: None or id of created ressource
        """
        # Check that require's fields are set
        for fieldname in self._columns:
            field = getattr(self, '_' + fieldname + '_field')
            if field.require and not self._fields[fieldname]:
                raise Core400Exception("Attribut '{}' is required".format(fieldname))

    def unlink(self):
        """ Delete the ressource. """
        domain = list()
        for identifier in self._identifiers:
            domain.append((identifier, '=', getattr(self, identifier)))

        self.delete(domain)
