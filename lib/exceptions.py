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


from .logger import error

"""
Exceptions are provided to send regular HTTP error code and messages.
If debug level is higher than 0 additionals informations will be send, otherwise standart HTTP messages are use.

To raise this kind of exception: ::

    raise Core400Exception("Additionals informations")

To handle this kind of excpetion: ::

    try:
        ...
    except Core404Exception as ex:
        print ex.code  # HTTP return code
        print ex.message  # HTTP message
        print ex.infos  # Additionals informations

"""


class CoreException(Exception):
    """
    Create a new core exception with HTTP return code.

    :param int code: HTTP return code.
    :param str message: HTTP return message.
    :param str infos: Error message.
    """
    def __init__(self, code, message, infos):
        self.code = code
        self.message = message
        self.infos = infos

    def __str__(self):
        return self.infos


class Core400Exception(CoreException):
    """ Create a 400 *Bad Request* exception.

    :param str infos: A message describing the error.
    """
    def __init__(self, infos):
        super(Core400Exception, self).__init__(400, 'Bad Request', infos)


class Core401Exception(CoreException):
    """ Create a 401 *Unauthorized* exception.

    :param str infos: A message describing the error.
    """
    def __init__(self, infos):
        super(Core401Exception, self).__init__(401, 'Unauthorized', infos)


class Core403Exception(CoreException):
    """ Create a 403 *Forbidden* exception.

    :param str infos: A message describing the error.
    """
    def __init__(self, infos):
        super(Core403Exception, self).__init__(403, 'Forbidden', infos)


class Core404Exception(CoreException):
    """ Create a 404 *Not Found* exception.

    :param str infos: A message describing the error.
    """
    def __init__(self, infos):
        super(Core404Exception, self).__init__(404, 'Not Found', infos)


class Core409Exception(CoreException):
    """ Create a 409 *Conflict* exception.

    :param str infos: A message describing the error.
    """
    def __init__(self, infos):
        super(Core409Exception, self).__init__(409, 'Conflict', infos)


class Core500Exception(CoreException):
    """ Create a 500 *Internal Server Error* exception.

    :param str infos: A message describing the error.
    """
    def __init__(self, infos):
        error(infos)
        super(Core500Exception, self).__init__(500, 'Internal Server Error', infos)


class ORMObjectNotFound(Core404Exception):
    """ Create a 404 *Not Found* exception for ORM object.

    :param str infos: A message describing the error.
    """
    def __init__(self, infos):
        super(ORMObjectNotFound, self).__init__(infos)
