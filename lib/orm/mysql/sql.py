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
import io
import uuid

from .sqlfilter import SQLFilter
from lib.exceptions import *
from lib.orm.fields import TimeField, BoolField, ImageField, BinaryField
from lib.orm.binary import Binary


class Sql(object):
    """ Generate SQL requests. """
    def _replaceSQL(self):
        f, v = self._prepareData()
        sql = "REPLACE INTO {}.{} ({})\n".format(self._dbname, self.__class__.__name__.lower(), ", ".join(f))
        sql += "VALUES ({});".format(", ".join(['%s' for i in range(0, len(f))]))
        return sql, v

    def _updateSQL(self, data2save, domain):
        f, v = self._prepareData(data2save)
        sqlFilter = SQLFilter(domain)

        if sqlFilter:
            sql = "UPDATE {}.{} ".format(self._dbname, self.__class__.__name__.lower())
            sql += "SET {} = %s ".format(" = %s, ".join(f))
            sql += "WHERE "
            sql += sqlFilter.condition
            sql += ";"
            v.extend(sqlFilter.data)
            return sql, v
        else:
            raise Core400Exception("Condition needed to process update")

    @classmethod
    def _deleteSQL(cls, domain):
        sqlFilter = SQLFilter(domain)
        if sqlFilter:
            sql = "DELETE FROM {}.{} ".format(cls._dbname, cls.__name__.lower())
            sql += "WHERE "
            sql += sqlFilter.condition
            sql += ";"
            return sql, sqlFilter.data
        else:
            raise Core400Exception("Condition needed to process delete")

    @classmethod
    def _selectSQL(cls, domain, fields=None, count=None, offset=None, sort=None):
        if fields and type(fields) is list:
            fields = ", ".join(set(cls._overrideColName(fields + cls._identifiers)))  # Always return identifiers
        else:
            fields = '*'

        if domain:
            sqlFilter = SQLFilter(domain)
            condition = sqlFilter.condition
            data = sqlFilter.data
        else:
            condition = "1"
            data = tuple()

        sql = "SELECT {} FROM {}.{} ".format(fields, cls._dbname, cls.__name__.lower())
        sql += "WHERE "
        sql += condition
        if sort:
            sql += " ORDER BY {}".format(", ".join(cls._overrideColName(sort)))
        if count and offset:
            sql += " LIMIT {}, {}".format(offset, count)
        elif count:
            sql += " LIMIT {}".format(count)
        sql += ";"
        return sql, data

    @classmethod
    def _createDatabaseSQL(cls):
        sql = "CREATE DATABASE IF NOT EXISTS {};".format(cls._dbname)
        return sql

    @classmethod
    def _dropDatabaseSQL(cls):
        sql = "DROP DATABASE IF EXISTS {};".format(cls._dbname)
        return sql

    @classmethod
    def _createTableSQL(cls):
        # TODO remove compute field from CREATE TABLE (resu of cls.__getColumnsSQL())
        sql = "CREATE TABLE IF NOT EXISTS {}.{} (\n".format(cls._dbname, cls.__name__.lower())
        sql += cls.__getColumnsSQL()
        sql += ") ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;"
        return sql

    @classmethod
    def _dropTableSQL(cls):
        return "DROP TABLE IF EXISTS {}.{};".format(cls._dbname, cls.__name__.lower())

    @classmethod
    def _overrideColName(cls, fields):
        f = list()

        for colname in fields:
            col = getattr(cls, "_{}_field".format(colname), None)
            if not col:
                raise Core404Exception("Attribute '" + colname + "' doesn't exist.")
            if not col.compute:
                f.append(col.fieldName or colname)

        return f

    @classmethod
    def _reverseData(cls, fields):
        """
        Replace SQL field name by python field name.
        Replace SQL value by python value.
        """
        for colname in cls._columns:
            col = getattr(cls, "_{}_field".format(colname), None)

            # Change field name
            name = col.fieldName
            if name in fields:
                fields[colname] = fields.pop(name)

            # Adapt Value
            if isinstance(col, TimeField) and colname in fields:
                fields[colname] = (datetime.datetime.min + fields[colname]).time()
            elif isinstance(col, BoolField) and colname in fields:
                fields[colname] = fields[colname] is 1
            elif isinstance(col, BinaryField) and colname in fields and fields[colname]:
                identifiers = list()
                for identifier in cls._identifiers:
                    ids = getattr(cls, "_{}_field".format(identifier))
                    ids = ids.fieldName or identifier
                    identifiers.append(str(fields[ids]))

                if col.backendFS:
                    metadata = fields[colname].split("\n")
                    fields[colname] = Binary(cls.__name__.lower(), colname, metadata[1], metadata[2], uuid=metadata[0])
                    fields[colname].loadStreamFromFS(identifiers)
                else:
                    if type(col) is ImageField:
                        fields[colname] = Binary(cls.__name__.lower(), colname, col.mimeType, col.extension, io.BytesIO(fields[colname]))
                        fields[colname].loadStreamFromDB(identifiers)
                    else:
                        data = fields[colname].split("\n", 2)
                        fields[colname] = Binary(cls.__name__.lower(), colname, data[0], data[1], io.BytesIO(data[2]))
                        fields[colname].loadStreamFromDB(identifiers)

    def _prepareData(self, data2save=None):
        """
        Field : Convert field name to SQL column name
        Value : Convert python type to SQL type
        """
        k = list()
        v = list()

        for colname in self._columns:
            col = getattr(self, "_{}_field".format(colname), None)
            if not col:
                raise Core404Exception("Attribute '" + colname + "' doesn't exist.")
            val = getattr(self, colname)

            # Use for UPDATE (partial fields), not for INSERT/REPLACE
            if data2save and (colname not in data2save):
                procceed = False
            else:
                procceed = True

            if not col.compute and val and procceed:
                # Colname
                k.append(col.fieldName or colname)

                # Value
                if type(val) is list:
                    v.append(",".join(val))
                elif type(val) is Binary:
                    if col.backendFS:
                        # Remove old file on FS before saving new one
                        if val.uuid:
                            val.removeStreamFromFS()
                        val.uuid = uuid.uuid4().hex

                        # data to FS
                        val.save()
                        # metadata to DB
                        v.append(val.uuid + "\n" + val.mimetype + "\n" + val.extension)
                    else:
                        if type(col) is ImageField:
                            v.append(val.stream.getvalue())
                        else:
                            data = io.BytesIO()

                            # metadata
                            data.write(str(val.mimetype))
                            data.write("\x0A")
                            data.write(str(val.extension))
                            data.write("\x0A")

                            # data
                            data.write(val.stream.getvalue())
                            v.append(data.getvalue())
                else:
                    v.append(val)

        return (k, v)

    @classmethod
    def __getColumnsSQL(cls):
        sql = ""

        for colname in cls._columns:
            col = getattr(cls, '_' + colname + '_field')
            name = col.fieldName or colname
            sql += getattr(Sql, "_{}__get{}SQL".format(Sql.__name__, col.__class__.__name__))(name, col)

        # Indexes
        sql += cls.__getIndexesSQL()

        # TODO gerer creation foreign key
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
                columns.append(col.fieldName or colname)

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
        elif col.default:
            default = str(col.default)

        if default:
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
        if col.length:
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
        default, null, unique = cls.__getColStruct(col)

        if col.backendFS:
            # Only metadata are store on DB
            sql = "{} {}{},\n".format(name, "TEXT", null)
        else:
            # Everything is store on DB
            sql = "{} {}{},\n".format(name, "BLOB", null)

        return sql

    @classmethod
    def __getImageFieldSQL(cls, name, col):
        return cls.__getBinaryFieldSQL(name, col)

    @classmethod
    def __getIntFieldSQL(cls, name, col):
        default, null, unique = cls.__getColStruct(col)
        if col.size or col.size < 12:
            t = "INT"
        else:
            t = "BIGINT"
        sqltype = col.backendType or t
        if col.size:
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
