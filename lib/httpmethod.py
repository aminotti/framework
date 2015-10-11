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
from flask import Response
from flask import request
from .exceptions import *


"""
from lib.jsonconvert import json2python, obj2json, dict2json
from config import conf

from lib.orm import ORMFilter, BinaryField, SQLRelationship, one2many
"""


class HTTPMethods(object):
    # TODO gerer different input et ouput (csv, json,...)
    __headers = {"Content-type": "application/json;charset=UTF-8"}

    """
    @classmethod
    def secureData(cls, data):
        for key, val in data.items():
            # Check field name
            if key not in cls._columns:
                raise Core400Exception("Bad attribute : '{}'".format(key))
            else:
                # Check value type & value syntax
                getattr(cls, key).check(val)
    """

    @classmethod
    def dispatchMethods(cls, condition=None, relationship=None):
        cond = condition
        """
        if type(condition) is dict:
            cls.secureData(condition)
            of = list()
            for key, val in condition.items():
                of.append(ORMFilter.eq(key, val))
            condition = ORMFilter.AND(of)
        elif condition is not None:
            raise Core400Exception("Invalid filter type : '{}'".format(str(condition)))
        """

        if request.method == 'GET':
            return cls._getHTTP(condition, relationship)
        elif request.method == 'PUT':
            if cond is None or sorted(cls._Identifiers) != sorted(cond.keys()):
                raise Core500Exception("Invalid identifiers.")
            return cls._putHTTP(condition, cond)
        elif request.method == 'PATCH':
            return cls._patchHTTP(condition)
        elif request.method == 'DELETE':
            return cls._deleteHTTP(condition)
        elif request.method == 'POST':
            return cls._postHTTP()

    @classmethod
    def _getHTTP(cls, condition=None, relationship=None):
        return "GET"
        """
        # Manage relashionship
        relationshipcls = None
        for relation in one2many[cls.__name__]:
            if relation.name is relationship:
                relationshipcls = relation.table
                break
        if relationshipcls is None and relationship is not None:
            raise Core500Exception("Bad relationship '{}'.".format(relationship))

        # Manage request arguement "fields"
        fields = request.args.get('fields', None)
        if fields is not None:
            fields = fields.split(",")
            if type(fields) is not list:
                raise Core400Exception("'{}' : bad type for fields.".format(fields))
            for name in fields:
                # Fields can be col of cls or name of a relationcls or if a relationship define, col of a relationship
                # if name not in cls._columns and name not in (d.name for d in one2many[cls.__name__]) and  and name not in relationshipcls._columns:
                if not (name in cls._columns or name in (d.name for d in one2many[cls.__name__]) or (relationshipcls and name in relationshipcls._columns)):
                    raise Core400Exception("Bad value '{}' in fields list.".format(name))

        # Manage request arguement "count"
        count = request.args.get('count', None)
        if count is not None:
            try:
                int(count)
            except ValueError:
                raise Core400Exception("'{}' : bad type for count.".format(count))

        # Manage request arguement "offset"
        offset = request.args.get('offset', None)
        if offset is not None:
            try:
                int(offset)
            except ValueError:
                raise Core400Exception("'{}' : bad type for offset.".format(offset))

        data = cls.get(condition, relationshipcls, fields, count, offset)
        print "# Instance", data[0].__dict__
        print "$$$$$", vars(data[0])
        print "# Class", data[0].__class__.__dict__
        if len(data) == 0:
            raise Core404Exception("Empty set")
        r = Response(obj2json(data), headers=cls.__headers)  # TODO change convert method according to client 'Accept' header
        r.status_code = 200
        return r
        """

    @classmethod
    def _postHTTP(cls):
        """
        dico = cls.getDataFromContentType()
        """

        ressource = cls(dico)
        idressource = ressource.create()

        if rowid is not None:
            url = request.base_url + '/' + str(rowid)  # TODO check que l'URL est bonne
            data = dict2json({"Location": url})
            r = Response(data, headers=cls.__headers)
        else:
            r = Response(None)
            del r.headers['content-type']
        r.status_code = 201
        return r

    # Complete ressource's update or creation
    @classmethod
    def _putHTTP(cls, domain, identifiers):
        """
        dico = cls.getDataFromContentType()
        if dico:
            dico.update(identifiers)
        else:
            dico = identifiers
        """
        # on à ajouté au dico le/les id de la ressouce et on creer un instance (pas besoin de lire la DB)

        ressource = cls(dico)
        ressource.write()

        r = Response(None)
        del r.headers['content-type']
        r.status_code = 204
        return r

    # Partial update on one or several ressource
    @classmethod
    def _patchHTTP(cls, domain):
        # dico = cls.getDataFromContentType() TODO

        ressource = cls(dico)
        cls.update(domain, ressource)

        r = Response(None)
        del r.headers['content-type']
        r.status_code = 204
        return r

    # Delete one or several ressource
    @classmethod
    def _deleteHTTP(cls, domain):
        cls.delete(domain)

        r = Response(None)
        del r.headers['content-type']
        r.status_code = 204
        return r

    """
    @classmethod
    def getDataFromContentType(cls):
        if 'application/json' in request.headers['Content-Type']:
            data = json2python(request.data)
            cls.secureData(data)
            return data
        elif 'multipart/form-data' in request.headers['Content-Type']:
            for val in request.form.values():
                dico = json2python(val)
                cls.secureData(dico)
            for key, val in request.files.items():
                # Check field name and type
                col = getattr(cls, key, None)
                if col is None or not isinstance(col, BinaryField):
                    raise Core400Exception("Bad binary attribute : '{}'".format(key))
                extension = os.path.splitext(val.filename)[1][1:]
                col.check(val.mimetype, extension)

                dico[key] = val
                return dico
        elif 'multipart/mixed' in request.headers['Content-Type']:
            # TODO Handle multipart/mixed
            print request.data
            return dict()
        elif '' in request.headers['Content-Type']:
            return None
        else:
            raise Core404Exception("Forbidden Content-Type '{}'. Accept only 'application/json' or 'multipart/form-data'".format(request.headers['Content-Type']))
    """
