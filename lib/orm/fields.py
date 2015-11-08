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


import io
import re
from PIL import Image
from datetime import datetime, date, time

from ..exceptions import *
from ..regex import *
from ..mimetype import MimeType


class Field(object):
    """ Base class for all Fields.

    :param str fieldName: Name of the field use in backend. If not set, the attribute's name is use in lower case.
    :param str label: Label for the field in forms. If not set, the field attribute's name (capitalized) is used.
    :param str help: Tooltip display to the user.
    :param default: Default python value for the field.
    :param bool identifier: Set to true if this field is an identifier.
    :param bool require: Set if a value for this field is require.
    :param bool copy: Whether the field value should be copied when the record is duplicated.
    :param bool unique: Set if the value for this field have to be unique.
    :param method compute: A method use to compute the field value. If compute is set, the value is not store in backend.
    :param method constraints: A method use to apply constraint on a field value (e.g. for int, check range between 1 and 100).
    :param method onchange: A method called on changing field value.
    :param bool index: Whether the field is indexed in backend.
    :param bool readwrite: Set ACI for read/write access.
    :param bool readonly: Set ACI for read-only access.
    :param str sqlType: To force a different backend type from python type.
    """

    regex = None
    """ Regular expression use to test string fields syntaxe. """

    def __init__(self,
                 fieldName=None,
                 label=None,
                 help=None,
                 default=None,
                 identifier=False,
                 require=True,
                 copy=True,
                 unique=False,
                 compute=None,
                 constraints=None,
                 onchange=None,
                 index=False,
                 readwrite=['*'],
                 readonly=['*'],
                 backendType=None):

        self.fieldName = fieldName
        self.label = label
        self.help = help
        self.default = default
        self.identifier = identifier
        if self.identifier:
            self.default = None
        self.require = require
        self.unique = unique
        self.copy = copy
        self.index = index
        self.constraints = constraints
        self.onchange = onchange
        self.compute = compute
        if self.compute:
            self.identifier = False
            self.default = None
            self.require = None
            self.constraints = None
            self.onchange = None
            self.index = False
            self.copy = False
            self.unique = False
        self.readwrite = readwrite
        self.readonly = readonly
        self.backendType = backendType

    def check(self, data):
        """ Method use to test field's value. Raise a 400 exception if test fail.

        :param str data: The field's value.
        """
        if data and self.regex:
            if self.regex.match(data) is None:
                raise Core400Exception("Invalid value : '{}'".format(data))


class BinaryField(Field):
    """ Create a new binary field.
    See :py:class:`Field` for extra arguments.

    :param list mimeTypes: List of allowed mime types, **default** are :py:attr:`~lib.mimetype.MimeType.openformat`.
    :param bool backendFS: True to store data on file system, False to store in database.

        .. attention::

            For LDAP backend, file are always store in LDAP.

    """
    def __init__(self, **kw):
        self.mimeTypes = kw.pop('mimeTypes', MimeType.openformat)
        if not MimeType.check(self.mimeTypes):
            raise Core500Exception("Unknow Mime Type : " + str(self.mimeTypes))
        self.backendFS = kw.pop('backendFS', False)
        super(BinaryField, self).__init__(**kw)

    def check(self, data):
        """ Verify that mime type is allowed and check that mime type and extension match.

        :param str mimeType: mime type of the binary file
        :param str extension: extension of the binary file
        """
        if data and data.mimetype not in self.mimeTypes:
            raise Core400Exception("Invalid mime types : '{}'".format(data.mimetype))
        if data and not MimeType.checkExtension(data.mimetype, data.extension):
            raise Core400Exception("Mime type and extension mismatch : '{} - {}'".format(data.mimetype, data.extension))


class ImageField(BinaryField):
    """ Create a new binary field.
    See :py:class:`Field` for extra arguments.

    :param list mimeTypes: List of allowed mime types for input, **default** are :py:attr:`~lib.mimetype.MimeType.image`.
    :param bool backendFS: See :py:class:`BinaryField`.
    :param str mimeType: mimeType for output, **default** to 'image/png'.
    :param str extension: file extension for output , **default** to 'png'.
    """
    def __init__(self, **kw):
        self.mimeTypes = kw.pop('mimeTypes', MimeType.image)
        self.mimeType = kw.pop('mimeType', 'image/png')
        self.extension = kw.pop('extension', 'png')
        if not MimeType.check(self.mimeTypes):
            raise Core500Exception("Unknow Mime Type : " + str(self.mimeType))
        if self.mimeType not in self.mimeTypes:
            raise Core500Exception("Mime Type : {} not in {}.".format(self.mimeType, str(self.mimeTypes)))
        if not MimeType.checkExtension(self.mimeType, self.extension):
            raise Core400Exception("Mime type and extension mismatch : '{} - {}'".format(self.mimeType, self.extension))

        if self.extension in ['jpg', 'jpeg', 'jpe']:
            self._PIL_filetype = "JPEG"
        elif self.extension in ['png']:
            self._PIL_filetype = "PNG"
        elif self.extension in ['gif']:
            self._PIL_filetype = "GIF"
        else:
            self._PIL_filetype = None

        super(ImageField, self).__init__(mimeTypes=self.mimeTypes, **kw)

    def convert(self, binary):
        """
        Convert a image to the type define in ``self.mineType``.

        :param Binary data: The stream to convert.

        .. note::

            Currently support conversion to PNG, JPEG, GIF.

            http://pillow.readthedocs.org/en/latest/handbook/image-file-formats.html

        """
        if self._PIL_filetype and binary.mimetype != self.mimeType:
            image = Image.open(binary.stream)
            # TODO implémenter la conversion à la bonne taille
            # image = image.resize((width, height))
            tmp = io.BytesIO()
            image.save(tmp, self._PIL_filetype)
            binary.stream = tmp
            binary.mimetype = self.mimeType
            binary.stream = tmp
            binary.extension = self.extension


class BoolField(Field):
    """ Create a new boolean field.
    See :py:class:`Field` for extra arguments.
    """
    def __init__(self, **kw):
        super(BoolField, self).__init__(**kw)

    def check(self, data):
        """ Raise a 400 exception if field's value is not a boolean.

        :param data: The field's value.
        """
        if date and type(data) is not bool:
            raise Core400Exception("Invalid boolean : '{}'".format(data))


class ColorField(Field):
    """ Create a new HTML color field.
    See :py:class:`Field` for extra arguments.
    """

    regex = HTMLColor
    """ Regular expression to test valid HTML color string. """

    def __init__(self, **kw):
        self.length = 15
        super(ColorField, self).__init__(**kw)


class CurrencyField(Field):
    """ Create a new currency field.
    See :py:class:`Field` for extra arguments.

    :param int size: number of digit, **default** to 10.
    :param int precision: number of decimal digit, **default** to 2.
    """
    def __init__(self, **kw):
        self.size = 10
        self.precision = 2
        super(CurrencyField, self).__init__(**kw)

    def check(self, data):
        """ Raise a 400 exception if field's value is not a currency value.

        :param data: The field's value.
        """
        if data:
            try:
                data = float(data)
            except ValueError:
                raise Core400Exception("Invalid currency : '{}'".format(data))


class DateField(Field):
    """ Create a new date field.
    See :py:class:`Field` for extra arguments.
    """

    regex = RFC3339.date
    """ Regular expression to test valid date string. """

    def __init__(self, **kw):
        super(DateField, self).__init__(**kw)

    def check(self, data):
        """ Raise a 400 exception if field's value is not a :py:class:`datetime.date`.

        :param data: The field's value.
        """
        if data and type(data) is not date:
            raise Core400Exception("Invalid date : '{}'".format(data))


class DatetimeField(Field):
    """ Create a new datetime field.
    See :py:class:`Field` for extra arguments.
    """

    regex = RFC3339.datetime
    """ Regular expression to test valid datetime string. """

    def __init__(self, **kw):
        super(DatetimeField, self).__init__(**kw)

    def check(self, data):
        """ Raise a 400 exception if field's value is not a :py:class:`datetime.datetime`.

        :param data: The field's value.
        """
        if data and type(data) is not datetime:
            raise Core400Exception("Invalid datetime : '{}'".format(data))


class DecimalField(Field):
    """ Create a new decimal field.
    See :py:class:`Field` for extra arguments.

    :param int size: number of digit, **default** to 10.
    :param int precision: number of decimal digit, **default** to 5.
    """
    def __init__(self, **kw):
        self.size = kw.pop('size', 10)
        self.precision = kw.pop('precision', 5)
        super(DecimalField, self).__init__(**kw)

    def check(self, data):
        """ Raise a 400 exception if field's value is not a decimal value.

        :param data: The field's value.
        """
        if data:
            try:
                data = float(data)
            except ValueError:
                raise Core400Exception("Invalid decimal : '{}'".format(data))


class EmailField(Field):
    """ Create a new email field.
    See :py:class:`Field` for extra arguments.

    :param int length: email max length, **default** to 255.
    """

    regex = MAIL
    """ Regular expression to test valid email address. """

    def __init__(self, **kw):
        self.length = 255
        super(EmailField, self).__init__(**kw)


class EnumField(Field):
    """ Create a new enum field.
    See :py:class:`Field` for extra arguments.

    :param list values: list all possible values, **default** to None.
    """
    def __init__(self, **kw):
        self.values = kw.pop('values', None)
        if self.values is None:
            raise Core500Exception("'value' is required for EnumCol")
        super(EnumField, self).__init__(**kw)

    def check(self, data):
        """ Raise a 400 exception if field's value is not a valid enum value.

        :param data: The field's value.
        """
        if type(data) is list:
            raise Core400Exception("Invalid type 'List' for EnumField value")
        elif not data or data.encode("utf8") not in self.values:
            raise Core400Exception("Invalid value : '{}'".format(data.encode("utf8")))


class ListField(Field):
    """ Create a new :py:class:`list` field.

    .. caution::

        Only list of string is supported.

    See :py:class:`Field` for extra arguments.


    :param str regex: regex, **default** protect against XSS attack.
    """
    def __init__(self, **kw):
        rx = kw.pop('regex', None)
        if rx is not None:
            self.regex = re.compile(rx)
        else:
            self.regex = XSS
        super(ListField, self).__init__(**kw)

    def check(self, data):
        """ Check the syntax of field's values.

        :param list data: The field's values.
        :raises Core400Exception: if the check failed.
        """
        if type(data) is not list:
            raise Core400Exception("Invalid List : '{}'".format(data))
        else:
            for val in data:
                if self.regex.match(val) is not None:
                    raise Core400Exception("Invalid value : '{}'".format(val))


class IntField(Field):
    """ Create a new integer field.
    See :py:class:`Field` for extra arguments.

    :param int size: number of digit, **default** to None.
    :param bool zerofill: for SQL, if fill with zero. **Default** to False.
    :param bool unsigned: for SQL, if number is signed or not. **Default** to False.
    :param bool autoIncrement: If auto increment is activate, not implemented by every backends. **Default** to False.
    """
    def __init__(self, **kw):
        self.size = kw.pop('size', None)
        self.zerofill = kw.pop('zerofill', False)
        self.unsigned = kw.pop('unsigned', False)
        self.autoIncrement = kw.pop('autoIncrement', False)
        if self.autoIncrement:
            kw['require'] = False
        super(IntField, self).__init__(**kw)

    def check(self, data):
        """ Raise a 400 exception if field's value is not a valid integer.

        :param data: The field's value.
        """
        if data:
            try:
                data = int(data)
            except ValueError:
                raise Core400Exception("Invalid integer : '{}'".format(data))


class SetField(Field):
    """ Create a new set field.
    See :py:class:`Field` for extra arguments.

    :param list values: list all possible values, **default** to None.
    """
    def __init__(self, **kw):
        self.values = kw.pop('values', None)
        if self.values is None:
            raise Core500Exception("'values' is required for SetCol")
        super(SetField, self).__init__(**kw)

    def check(self, data):
        """ Raise a 400 exception if field's value is not a valid set.

        :param data: The field's value.
        """
        if type(data) is not list:
            raise Core400Exception("Invalid set : '{}'".format(data))
        else:
            for val in data:
                if val.encode("utf8") not in self.values:
                    raise Core400Exception("Invalid value : '{}'".format(val.encode("utf8")))


class StringField(Field):
    """ Create a new string field.
    See :py:class:`Field` for extra arguments.

    :param str length: max length of the string, **default** to None.
    :param str regex: regex, **default** protect against XSS attack.
    """
    def __init__(self, **kw):
        self.length = kw.pop('length', None)
        rx = kw.pop('regex', None)
        if rx is not None:
            self.regex = re.compile(rx)
        else:
            self.regex = XSS
        super(StringField, self).__init__(**kw)

    def check(self, data):
        """ Raise a 400 exception if syntax of field's value is not valid.

        :param data: The field's value.
        """
        if data and self.regex.match(data) is not None:
            raise Core400Exception("Invalid value : '{}'".format(data))


class PhoneField(Field):
    """ Create a new phone number field.
    See :py:class:`Field` for extra arguments.

    :param str length: max number of character, **default** to 20.
    """

    regex = PHONE
    """ Regular expression to test valid phone number. """

    def __init__(self, **kw):
        self.length = 20
        super(PhoneField, self).__init__(**kw)


class TimeField(Field):
    """ Create a new time field.
    See :py:class:`Field` for extra arguments.
    """

    regex = RFC3339.time
    """ Regular expression to test valid time string. """

    def __init__(self, **kw):
        super(TimeField, self).__init__(**kw)

    def check(self, data):
        """ Raise a 400 exception if field's value is not a :py:class:`datetime.time`.

        :param data: The field's value.
        """
        if data and type(data) is not time:
            raise Core400Exception("Invalid time : '{}'".format(data))


class UrlField(Field):
    """ Create a new URL field.
    See :py:class:`Field` for extra arguments.

    :param str length: URL max length, **default** to 2048.
    """

    regex = URL
    """ Regular expression to test valid URL. """

    def __init__(self, **kw):
        self.length = 2048
        super(UrlField, self).__init__(**kw)


class Index(object):
    """ Create a new Index base on several Fields.

    .. note::

        * Indexes are automatically created for identifiers.
        * For Index on single Field, use Field's attribute instead.

    :param columns: list of str containing field's name.
    """
    def __init__(self, columns):
        self.columns = columns
