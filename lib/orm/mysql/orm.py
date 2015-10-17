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

import pymysql
from pymysql.err import *
from ..base import Mapper
from .sql import Sql
from ..pool import ConnectionInfos, Pool
from ...logger import debug
from app.config import conf
from lib.exceptions import *


class ORM(Mapper, Sql):
    @classmethod
    def setupConnection(cls, uri, tenant):
        scheme, user, pwd, host, port, dbname = cls.parseURI(uri)
        port = port or 3306

        if conf.multi_tenancy:
            _dbname = "{}_{}".format(dbname, tenant)
        else:
            _dbname = dbname

        _connection_name = "{}://{}@{}".format(scheme, user, host)

        debug("Adding '{}' to pools".format(_connection_name))
        connection_infos = ConnectionInfos(pymysql, _connection_name, host=host, port=port, user=user, password=pwd, autocommit=True, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        Pool.add(connection_infos)

        return dict({'_dbname': _dbname, '_connection_name': _connection_name})

    @classmethod
    def parseURI(cls, uri):
        infos = super(ORM, cls).parseURI(uri)
        # TODO Eventuellement parser les params (infos[5]) pour recup db options (genre charset, autocommit,...)
        return infos

    @staticmethod
    def whoami():
        return "MySQL"

    @classmethod
    def onInstall(cls):
        # TODO create table if not exist
        # TODO exec add columns ALTER TABLE `users` ADD `date` DATE NULL DEFAULT NULL ;
        # TODO si failure exec modify columns ALTER TABLE `users` MODIFY `date` DATE NULL DEFAULT NULL ;
        # add columns or modify columns
        # cls._exeSQL(cls._dropTableSQL())
        cls._exeSQL(cls._createTableSQL())

    @classmethod
    def update(cls, domain, ressource):
        # Parent method check data and return secured data to save
        data2save = super(ORM, cls).update(domain, data)

    def write(self):
        # Parent method test if require fields are set
        super(ORM, self).write()

    @classmethod
    def _insertSQL(cls, request, data=tuple()):
        """ Return last ID created """
        c = cls._query(request, data)
        return c.lastrowid

    @classmethod
    def _selecSQL(cls, request, data=tuple()):
        """ return selected data """
        c = cls._query(request, data)
        return c.fetchall()

    @classmethod
    def _exeSQL(cls, request, data=tuple()):
        """ Execute update and delete request
        return number of row affected
        """
        c = cls._query(request, data)
        return c.rowcount

    @classmethod
    def _query(cls, request, data=tuple()):
        conn = Pool.getConnection(cls._connection_name)

        try:
            c = conn.cursor()
            debug(request + " " + str(data))
            c.execute(request, data)
            debug(c._last_executed)
        except IntegrityError as e:
            result = None
            raise Core400Exception(repr(e))
        except Exception as e:
            if e.args[0] in [2006, 2013, 2055]:
                Pool.getPurge(cls._connection_name)
            result = None
            raise Core500Exception(repr(e))
        # Put back to pool
        conn.close()
        # return result
        return c
