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

import datetime


class Sql(object):
    """ Generate SQL requests. """
    @classmethod
    def _createTableSQL(cls):
        sql = "CREATE TABLE IF NOT EXISTS {}.{} (\n".format(cls._dbname, cls.__name__.lower())
        sql += cls.__getColumnsSQL()
        sql += ") ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;"
        return sql

    @classmethod
    def _dropTableSQL(cls):
        return "DROP TABLE IF EXISTS {}.{};".format(cls._dbname, cls.__name__.lower())

    @classmethod
    def __getColumnsSQL(cls):
        sql = ""

        for colname in cls._columns:
            col = getattr(cls, '_' + colname + '_field')
            name = col.fieldName or colname.lower()
            sql += getattr(Sql, "_{}__get{}SQL".format(Sql.__name__, col.__class__.__name__))(name, col)

        # Indexes
        sql += cls.__getIndexesSQL()

        """
        # Foreign keys
        for fk in lib.orm.one2many[sqlcls.__name__]:
            if fk.cascade:
                cascade = "ON UPDATE CASCADE ON DELETE CASCADE"
            else:
                cascade = "ON UPDATE NO ACTION ON DELETE NO ACTION"

            if fk.table.connectionInfos:
                db = fk.table.connectionInfos.databaseName
            else:
                db = self._database

            sql += "FOREIGN KEY ({}) REFERENCES {}.{}({}) {},\n".format(",".join(fk.table._Identifiers), db, fk.table._tableName, ",".join(fk.table._Identifiers), cascade)
        """
        # Primary keys
        sql += "PRIMARY KEY ({})\n".format(",".join(cls._identifiers))

        return sql

    @classmethod
    def __getIndexesSQL(cls):
        if not cls._indexes:
            return ""

        sql = ""
        for idxname in cls._indexes:
            # Retrieve column's mame
            index = getattr(cls, idxname)
            if type(index.columns) is not list:
                cols = [index.columns]
            else:
                cols = index.columns

            # Check if column's name is different from SQL column's name
            columns = list()
            for colname in cols:
                col = getattr(cls, "_" + colname + "_field")
                columns.append(col.fieldName or colname.lower())

            sql += "INDEX {} ({}),\n".format(idxname, ",".join(columns))

        return sql

    @classmethod
    def __getColStruct(cls, col):
        default = col.default

        if type(col.default) is list:
            default = ",".join(col.default)
        elif type(col.default) is bool:
            if col.default:
                default = '1'
            else:
                default = '0'
        elif col.default is not None:
            default = str(col.default)

        if default is not None:
            default = " DEFAULT '{}'".format(default.replace("'", "''"))
        else:
            default = ""
        if col.require:
            null = " NOT NULL"
        else:
            null = " NULL"
        if col.unique:
            unique = " UNIQUE KEY"
            null = " NOT NULL"
            default = ""
        else:
            unique = ""
        if col.identifier:
            null = " NOT NULL"

        return (default, null, unique)

    @classmethod
    def __getStringFieldSQL(cls, name, col):
        default, null, unique = cls.__getColStruct(col)
        if col.length is None or col.length > 2000:
            t = "TEXT"
            default = ""
        else:
            t = "VARCHAR"
        sqltype = col.backendType or t
        if col.length is not None:
            length = "({})".format(col.length)
        else:
            length = ""
        if sqltype == "TEXT":
            default = ""
            length = ""
        return "{} {}{}{}{}{},\n".format(name, sqltype, length, null, default, unique)

    @classmethod
    def __getURLFieldSQL(cls, name, col):
        return cls.__getStringFieldSQL(name, col)

    @classmethod
    def __getEmailFieldSQL(cls, name, col):
        return cls.__getStringFieldSQL(name, col)

    @classmethod
    def __getColorFieldSQL(cls, name, col):
        return cls.__getStringFieldSQL(name, col)

    @classmethod
    def __getPhoneFieldSQL(cls, name, col):
        return cls.__getStringFieldSQL(name, col)

    @classmethod
    def __getSetFieldSQL(cls, name, col):
        default, null, unique = cls.__getColStruct(col)
        sqltype = "SET"
        values = "('{}')".format("','".join(col.values))
        return "{} {}{}{}{}{},\n".format(name, sqltype, values, null, default, unique)

    @classmethod
    def __getEnumFieldSQL(cls, name, col):
        default, null, unique = cls.__getColStruct(col)
        sqltype = "ENUM"
        values = "('{}')".format("','".join(col.values))
        return "{} {}{}{}{}{},\n".format(name, sqltype, values, null, default, unique)

    @classmethod
    def __getDecimalFieldSQL(cls, name, col):
        default, null, unique = cls.__getColStruct(col)
        sqltype = "DECIMAL"
        return "{} {}({},{}){}{}{},\n".format(name, sqltype, col.size, col.precision, null, default, unique)

    @classmethod
    def __getCurrencyFieldSQL(cls, name, col):
        return cls.__getDecimalFieldSQL(name, col)

    @classmethod
    def __getBinaryFieldSQL(cls, name, col):
        # TODO gerer binary field pour create columns
        """
        # la colone contiendra les métadonnées du fichier, si backendFS est a False alors on créer un blob pour stocker le fichier
        default, null, unique = cls.__getColStruct(col)
        sql = "{} {}{},\n".format(name, "VARCHAR(255)", null)
        if not col.backendFS:
            sql += "{}_data {}{},\n".format(name, "BLOB", null)
        return sql
        """
        return ""

    @classmethod
    def __getImageFieldSQL(cls, name, col):
        return cls.__getBinaryFieldSQL(name, col)

    @classmethod
    def __getIntFieldSQL(cls, name, col):
        default, null, unique = cls.__getColStruct(col)
        if col.size is None or col.size < 12:
            t = "INT"
        else:
            t = "BIGINT"
        sqltype = col.backendType or t
        if col.size is not None:
            size = "({})".format(col.size)
        else:
            size = ""
        if col.zerofill:
            zerofill = " ZEROFILL"
        else:
            zerofill = ""
        if col.unsigned:
            unsigned = " UNSIGNED"
        else:
            unsigned = ""
        if col.autoIncrement:
            autoIncrement = " AUTO_INCREMENT"
            null = " NOT NULL"
            default = ""
            unique = ""
        else:
            autoIncrement = ""
        return "{} {}{}{}{}{}{}{}{},\n".format(name, sqltype, size, unsigned, zerofill, null, autoIncrement, default, unique)

    @classmethod
    def __getBoolFieldSQL(cls, name, col):
        default, null, unique = cls.__getColStruct(col)
        sqltype = "TINYINT(1)"
        return "{} {}{}{}{},\n".format(name, sqltype, " NOT NULL", default, unique)

    @classmethod
    def __getDateFieldSQL(cls, name, col):
        default, null, unique = cls.__getColStruct(col)
        sqltype = "DATE"
        return "{} {}{}{}{},\n".format(name, sqltype, null, default, unique)

    @classmethod
    def __getTimeFieldSQL(cls, name, col):
        default, null, unique = cls.__getColStruct(col)
        sqltype = "TIME"
        return "{} {}{}{}{},\n".format(name, sqltype, null, default, unique)

    @classmethod
    def __getDatetimeFieldSQL(cls, name, col):
        default, null, unique = cls.__getColStruct(col)
        sqltype = "DATETIME"
        return "{} {}{}{}{},\n".format(name, sqltype, null, default, unique)
