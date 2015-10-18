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
from lib import contenttype
# from lib.orm import ORMFilter, BinaryField, SQLRelationship, one2many


class HTTPMethods(object):
    # TODO gerer different input et ouput de facon modulaire (csv, json, bjson...)
    # TODO Gerer les accept et content type header
    __headers = {"Content-type": "application/json;charset=UTF-8"}

    @classmethod
    def dispatchMethods(cls, domain=None, relationship=None):
        if domain:
            cls._checkDomains(domain)

        if request.method == 'GET':
            return cls._getHTTP(domain, relationship)
        elif request.method == 'PUT':
            return cls._putHTTP(domain)
        elif request.method == 'PATCH':
            return cls._patchHTTP(domain)
        elif request.method == 'DELETE':
            return cls._deleteHTTP(domain)
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

    # Ressource creation with auto id
    @classmethod
    def _postHTTP(cls):
        dico = cls.getDataFromContentType()

        ressource = cls(dico)
        ressource.write()

        r = Response(None)
        del r.headers['content-type']
        r.status_code = 201
        return r

    # Ressource creation with ids provided
    @classmethod
    def _putHTTP(cls, domain):
        dico = cls.getDataFromContentType()
        if type(dico) is not dict:
            raise Core400Exception("Bad content.")

        ressource = cls(dico)
        ressource.setIdFromDomain(domain)
        ressource.write()

        r = Response(None)
        del r.headers['content-type']
        r.status_code = 201
        return r

    # Update on one or several ressource
    @classmethod
    def _patchHTTP(cls, domain):
        dico = cls.getDataFromContentType()

        ressource = cls(dico)
        ressource.update(dico.keys(), domain)

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

    @classmethod
    def getDataFromContentType(cls):
        # http://www.w3.org/Protocols/rfc1341/4_Content-Type.html
        """ Devrais accepter que multipart/form-data, multipart/mixed,type defini dans lib.contenttype ou binaire
            multipart/form-data et multipart/mixed devrais accepter que type defini dans lib.contenttype et binaire
            Type binaire :
            * GET|PUT /binary/<ressource>/<id1>[/<id2>]/attribute.ext
            * del quand lattribut de la ressource est set a NULL (au lieux de contenir URL)
        """
        for ctype, conv in contenttype.Converter.items():
            if ctype in request.headers['Content-Type']:
                return conv.toDict(request.data)
                break

        if 'multipart/form-data' in request.headers['Content-Type']:
            pass  # TODO implementaire pour binary
            return dict()
            """
            for val in request.form.values():
                dico = json2python(val)
            for key, val in request.files.items():
                # Check field name and type
                col = getattr(cls, key, None)
                if col is None or not isinstance(col, BinaryField):
                    raise Core400Exception("Bad binary attribute : '{}'".format(key))
                extension = os.path.splitext(val.filename)[1][1:]
                col.check(val.mimetype, extension)

                dico[key] = val
                return dico
            """
        elif 'multipart/mixed' in request.headers['Content-Type']:
            # TODO Handle multipart/mixed
            print request.data
            return dict()
        else:
            raise Core404Exception("Forbidden Content-Type '{}'".format(request.headers['Content-Type']))

    @classmethod
    def _checkDomains(cls, domain):
        if type(domain) is tuple:
            cls._checkDomainTuple(domain)
        elif type(domain) is list:
            cls._checkDomainList(domain)
        else:
            raise Core400Exception("Invalid domain : {}, Must be list or tuple".format(str(domain)))

    @classmethod
    def _checkDomainList(cls, domain):
        for dom in domain:
            if type(dom) is str and dom in ['|', '&']:
                pass
            elif type(dom) is tuple:
                cls._checkDomainTuple(dom)
            elif type(dom) is list:
                cls._checkDomainList(dom)
            else:
                raise Core500Exception("Invalid domain part : {}".format(str(dom)))

    @classmethod
    def _checkDomainTuple(cls, domain):
        if len(domain) != 3:
            raise Core500Exception("Invalid tuple for domain {}".format(domain))

        # Check field name
        if domain[0] not in cls._columns:
            raise Core400Exception("Bad attribute : '{}'".format(domain[0]))
        else:
            # Check value type & value syntax
            getattr(cls, "_{}_field".format(domain[0])).check(domain[2])
