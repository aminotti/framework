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
import shutil
from flask import Flask, Response, request
from .config import conf
from .models import sysmod
import app.context  # Prevent cross import lib.model & app.context & Builder
from lib.model import Builder
from lib.orm.pool import Pool


manager = Flask(__name__)


@manager.route('/tenants/<tenant>/', methods=["PUT", "DELETE"])
def manage_tenant(tenant):
    r = Response(None)
    mod = __import__('lib.orm.{}'.format(Builder.getScheme(conf.db_uri)), globals(), locals(), ['ORM'], -1)
    base = mod.ORM

    if not conf.multi_tenancy:
        tenant = "yameo"

    directory = os.path.join(conf.data_dir, tenant)

    # Need a ressource class to create or destroy backend
    dico = sysmod['Addons'].copy()
    dico.update(base.setupConnection(conf.db_uri, tenant))
    ressource = type('Addons', (base, ), dico)
    Pool.build(conf.max_pool_size)

    if request.method == 'PUT':
        # Create default database
        ressource.createBackend()

        # Load system models and create Tables
        ressource.onInstall()
        for name, dico in sysmod.items():
            d = dico.copy()
            d.update(base.setupConnection(dico['_uri'], tenant))
            cls = type(name, (base, ), d)
            cls.onInstall()

        # Create data directory
        if not os.path.exists(directory):
            os.makedirs(directory)

        r.status_code = 201
    else:
        # Remove default database
        ressource.destroyBackend()

        # Remove data directory
        if os.path.exists(directory):
            shutil.rmtree(directory)

        r.status_code = 204

    del r.headers['content-type']
    return r
