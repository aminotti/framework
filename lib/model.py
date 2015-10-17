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

from lib.exceptions import *
import lib.orm.fields
from app.config import conf
from flask import request
import app.context


class Builder(object):
    @classmethod
    def get(cls, name, model, tenant):
        d = dict()  # dictionnary's attribute exclude from inherance
        f = dict()  # Fields, indexes and function (use for inherance)
        fields = dict()
        indexes = dict()
        for data in model:
            if 'inherit' not in data:
                data['inherit'] = None

            del data['sequence']

            # override index
            indexes.update(data.pop('indexes', dict()))

            # override fields
            attrs = data.pop('fields')
            for key, val in attrs.items():
                if key in fields:
                    fields[key].update(val)
                else:
                    fields[key] = val

            # override functions
            fcts = data.pop('functions')
            for key, val in fcts.items():
                f[key] = val

            # override private attribute
            for k, v in data.items():
                d['_' + k] = v

        for k, v in indexes.items():
            f[k] = lib.orm.fields.Index(v)

        for k, v in fields.items():
            f[k] = cls._buildField(v)

        d['_uri'] = cls._setURI(d.get('_uri', 'default'))
        mod = __import__('lib.orm.{}'.format(cls.getScheme(d['_uri'])), globals(), locals(), ['ORM'], -1)
        b = mod.ORM

        return (name, (b,), d, f)

    @classmethod
    def _setURI(cls, uri):
        """ Retrieve a correct working URI """
        # Set default URI to global conf
        if uri == 'default':
            return conf.db_uri

        # Handle config://global_conf_name
        scheme, var = uri.split('://', 1)
        if scheme == 'config':
            return getattr(conf, var, conf.db_uri)
        else:
            return uri

    @staticmethod
    def getScheme(uri):
        if '://' not in uri:
            raise Core500Exception("Bad syntax : {}".format(uri))
        return uri.split('://', 1)[0]

    @staticmethod
    def _buildField(data):
        fieldtype = "{}Field".format(data.pop('type').capitalize())
        class_ = getattr(lib.orm.fields, fieldtype)
        return class_(**data)


def default_routes(*args, **kwargs):
    name = str(request.url_rule).split('/')[1].capitalize()
    ressource = app.context.models.get(name)

    domain = list()
    for key, val in kwargs.items():
        domain.append((key, '=', val))

    return ressource.dispatchMethods(domain)


def default_post_routes():
    name = str(request.url_rule).split('/')[1].capitalize()
    ressource = app.context.models.get(name)

    return ressource.dispatchMethods()
