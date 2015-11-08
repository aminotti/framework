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
from lib.orm.binary import Binary
from lib.orm.fields import BinaryField
# from lib.orm import ORMFilter, BinaryField, SQLRelationship, one2many


class HTTPMethods(object):
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
    def _getHTTP(cls, domain=None, relationship=None):
        # TODO add expend = True pour toucher les relation au lieux de leur id
        # TODO ajouter un attribute expend = request.args.get('expend', False) pour geré si renvoi url des relations ou data completes
        """
        # Manage relashionship
        relationshipcls = None
        for relation in one2many[cls.__name__]:
            if relation.name is relationship:
                relationshipcls = relation.table
                break
        if relationshipcls is None and relationship is not None:
            raise Core500Exception("Bad relationship '{}'.".format(relationship))
        """

        # Manage request arguement "fields"
        fields = request.args.get('fields', None)
        if fields:
            fields = fields.split(",")
            if type(fields) is not list:
                raise Core400Exception("'{}' : bad type for fields.".format(fields))
            for name in fields:
                # Fields can be col of cls or name of a relationcls or if a relationship define, col of a relationship
                # if not (name in cls._columns or name in (d.name for d in one2many[cls.__name__]) or (relationshipcls and name in relationshipcls._columns)):
                if not (name in cls._columns):
                    raise Core400Exception("Bad value '{}' in fields list.".format(name))

        # Check request's arguement "count"
        count = request.args.get('count', None)
        if count:
            try:
                int(count)
            except ValueError:
                raise Core400Exception("'{}' : bad type for count.".format(count))

        # Check request's arguement "offset"
        offset = request.args.get('offset', None)
        if offset:
            try:
                int(offset)
            except ValueError:
                raise Core400Exception("'{}' : bad type for offset.".format(offset))

        # Check request's arguement "sort"
        sort = request.args.get('sort', None)
        if sort:
            sort = sort.split(",")
            for f in sort:
                if f not in cls._columns:
                    raise Core400Exception("Can't sort on {}. Field doesn't exist.".format(f))

        # TODO Set ressource language : request 'Accept-Language' and set reponse 'Content-Language'
        # langs = cls._orderHeaderByq(request.headers['Accept-Language'])  # Return list of lang order by preference, Firt item is prefered one.

        ressources = cls.search(domain, fields, count, offset, sort)
        if len(ressources) == 0:
            raise Core404Exception("Empty set")

        data = list()
        if fields:
            fields += cls._identifiers
        for r in ressources:
            # create dict from all ressource's fields or selected field in request arg if provided
            data.append(dict([(f, r._fields[f]) for f in (fields or cls._columns)]))

        ctype, Converter = cls._getAcceptedContentType()
        r = Response(Converter.fromDict(data), headers={"Content-type": "{};charset=UTF-8".format(ctype)})
        r.status_code = 200
        return r

    # Ressource creation with auto id
    @classmethod
    def _postHTTP(cls):
        dico = cls.getDataFromContentType()

        ressource = cls(dico)
        rid = ressource.create()

        if rid:
            url = request.base_url + str(rid) + '/'
            data = {"Location": url}

            ctype, Converter = cls._getAcceptedContentType()
            r = Response(Converter.fromDict(data), headers={"Content-type": "{};charset=UTF-8".format(ctype)})
        else:
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
        ressource.create()

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
    def _getAcceptedContentType(cls):
        accepts = cls._orderHeaderByq(request.headers['Accept'])
        for accept in accepts:
            if accept in contenttype.Converter.keys():
                return accept, contenttype.Converter[accept]
                break

        # Default content type is JSON
        # TODO RFC2616 sect 14.1, si wrong 'Accept' header : 406 (Not Acceptable). Si * ou pas de 'Accept' alors default json
        return "application/json", contenttype.Converter["application/json"]

    @classmethod
    def _orderHeaderByq(cls, header):
        """ Order HTTP header by preference set with q=number

        ;return list: ordered list with firsts items as prefered
        """
        ordered = dict()

        for part in header.split(","):
            subpart = part.split(";")
            if len(subpart) > 1 and "q=" in subpart[1]:
                try:
                    ordered[subpart[0].strip()] = float(subpart[1].strip()[2:])
                except ValueError:
                    raise Core400Exception("'{}' : q must be a number.".format(subpart[1].strip()))
            else:
                ordered[subpart[0].strip()] = 1.0

        return sorted(ordered, key=ordered.__getitem__, reverse=True)

    @classmethod
    def getDataFromContentType(cls):
        # http://www.w3.org/Protocols/rfc1341/4_Content-Type.html
        """ Devrais accepter que multipart/form-data, multipart/mixed,type defini dans lib.contenttype ou binaire
            multipart/form-data et multipart/mixed devrais accepter que type defini dans lib.contenttype et binaire
            Type binaire :
            * GET|PUT /binary/<ressource>/<id1>[/<id2>]/attribute.ext
            * del quand lattribut de la ressource est set a NULL (au lieux de contenir URL)
        """
        # TODO documenter les different content-type possible avec leur contenu de body
        for ctype, conv in contenttype.Converter.items():
            if ctype in request.headers['Content-Type']:
                return conv.toDict(request.data)
                break
        if 'application/x-www-form-urlencoded' in request.headers['Content-Type']:
            # TODO gerer POST normal (x-www-form-urlencode) formulaire (voir tests/form.html)
            print request.data
            return dict()
        elif 'multipart/form-data' in request.headers['Content-Type']:
            for val in request.form.values():
                # TODO Actuelement un seul attribut de form envoyer qui contient un json avec tout les fields :
                # - Remplacer par : un attribut de form par field (plus de notion de content type) => voir tests/form_file.html
                # - Gerer les contents type des sous part (json, xml, file,...) avec 'multipart/mixed'
                dico = contenttype.Converter['application/json'].toDict(val)
            for key, val in request.files.items():
                # Check field name and type
                col = getattr(cls, "_{}_field".format(key), None)
                if col is None or not isinstance(col, BinaryField):
                    raise Core400Exception("Bad binary attribute : '{}'".format(key))

                binary = Binary(key, val.mimetype, os.path.splitext(val.filename)[1][1:], val.stream)

                dico[key] = binary
                return dico
        elif 'multipart/mixed' in request.headers['Content-Type']:
            # TODO Handle multipart/mixed, faire une lib pour gere corp http/mail :
            # Extract boundary from content-type headers
            # parse request.data with boundary to get dict() : {'subcontenttype1': 'data1', 'subcontenttype2':'data2', ...}
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
