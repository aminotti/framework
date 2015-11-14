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
import io
import os
import shutil
from werkzeug import secure_filename
from flask import current_app, send_file, request, Response
from .controller import Controller
from .context import models
from .module import SmartManagement
from lib.exceptions import *
from lib.orm.binary import Binary
from .config import conf


ctl = Controller()
# TODO gerer les permissions sur toutes les routes


@ctl.route('/binaries/<ressource>/<path:ids>/<filename>', methods=['GET', 'PUT', 'PATCH'])
def getBinariesFiles(ressource, ids, filename):
    ids = ids.split('/')
    attribute, extension = os.path.splitext(secure_filename(filename))
    ressource = ressource.capitalize()

    res = models.get(ressource)
    if not res:
        raise Core404Exception("Ressource '{}' not found.".format(ressource))

    res = res.get(*ids)

    if not res:
        raise Core404Exception("Ressource with ids '{}' not found.".format(ids))

    if request.method == 'GET':
        field = getattr(res, attribute.lower(), None)

        if not field:
            raise Core404Exception("'{}' of ressource '{}' not found.".format(attribute, ressource))

        if field.extension != extension[1:]:
            raise Core404Exception("File {}{} not found.".format(attribute, extension))

        return send_file(field.stream, field.mimetype)
    else:
        if attribute.lower() not in res._columns:
            raise Core400Exception("Bad binary attribute : '{}'".format(attribute))

        binary = Binary(ressource.lower(), attribute, request.headers['Content-Type'], extension[1:], io.BytesIO(request.data))
        setattr(res, attribute.lower(), binary)
        res.write()

        r = Response(None)
        del r.headers['content-type']
        r.status_code = 204
        return r


@ctl.route('/')
def yameo_hello():
    return "Hello {}!".format(current_app.tenant)


"""
@ctl.route('/yameo/install/<module>/')
def yameo_install(module):
    SmartManagement.install(module, current_app)
    return "Install ok!!"
"""


# TESTS :


@ctl.route('/yameo/booking/<int:code>/')
def yameo_test(code):
    book = models.Booking.get(code)
    if book:
        return book.name
        # book.unlink()
    else:
        return "Booking {} pas trouvé, devrais ernvoyer un 404!".format(code)
