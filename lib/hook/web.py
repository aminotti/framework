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


import urllib2
from lib import contenttype
from ..logger import debug, error


class Web(object):

    @classmethod
    def runCreate(cls, ressource_name, settings, data):
        debug("Proceed Web Hook for {} created".format(ressource_name))
        return cls._exeRequest(settings, ressource_name, 'created', data)

    @classmethod
    def runUpdate(cls, ressource_name, settings, identifiers, data):
        debug("Proceed Web Hook for {} updated".format(ressource_name))
        return cls._exeRequest(settings, ressource_name, 'updated', {"identifiers": identifiers, "data": data})

    @classmethod
    def runDelete(cls, ressource_name, settings, identifiers):
        debug("Proceed Web Hook for {} deleted".format(ressource_name))
        return cls._exeRequest(settings, ressource_name, 'deleted', {"identifiers": identifiers})

    @classmethod
    def _exeRequest(cls, settings, ressource, event, data=None):
        try:
            req = urllib2.Request(settings['url'])
            req.add_header('User-agent', 'Yameo Hook')
            if data:
                if "mimetype" in settings:
                    mimetype, body = cls._convert2Minetype(data, settings['mimetype'])
                else:
                    mimetype, body = cls._convert2Minetype(data)
                req.add_header('Content-Type', mimetype)
            else:
                body = None

            req.add_header('X-Yameo-Ressource', ressource)
            req.add_header('X-Yameo-Event', event)
            if 'headers' in settings:
                for key, val in settings['headers'].items():
                    # Only a few headers are allowed
                    if key in ["Authorization"]:
                        req.add_header(key, val)

            response = urllib2.urlopen(req, body)
            return "{} {}".format(response.code, response.msg)
        except urllib2.HTTPError as err:
            msg = "{} {}".format(err.code, err.msg)
            error("Web Hook for {} {} : {}".format(ressource, event, msg))
            return msg

    @classmethod
    def _convert2Minetype(cls, data, mimetype="application/json"):
        if mimetype not in contenttype.Converter.keys():
            minetype = "application/json"

        converter = contenttype.Converter[mimetype]
        return mimetype, converter.fromDict(data)
