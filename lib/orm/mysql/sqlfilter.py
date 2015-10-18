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


class SQLFilter(object):
    """ Convert domain to SQL WHERE clause
    Domain syntax can be :

    * ('field1', '=', 5)  # Simple condition
    * [('field1', '=', 5), ('field2', '=', 10)]  # AND
    * ['|', ('field1', '=', 5), ('field2', '=', 10)]  # OR
    * ['|', ('field1', '=', 5), ['&', ('field2', '!=', 10), ('field3', '=', '12')]]  # Combined condition

    """
    def __init__(self, domain):
        if type(domain) is tuple:
            condition, data = self._parseTuple(domain)
        elif type(domain) is list:
            condition, data = self._parseList(domain)
        else:
            raise Core500Exception("Invalid domain : {}, Must be list or tuple".format(str(domain)))

        self.condition = condition
        self.data = tuple(data)

    def _parseList(self, domain):
        condition = list()
        data = list()

        if type(domain[0]) is str:
            if domain[0] is '|':
                domain.pop(0)
                operator = ' OR '
            elif domain[0] is '&':
                domain.pop(0)
                operator = ' AND '
            else:
                raise Core500Exception("Invalid operator {} in {}".format(domain[0], str(domain)))
        else:
            operator = ' AND '

        for dom in domain:
            if type(dom) is tuple:
                cond, d = self._parseTuple(dom)
                data.extend(d)
                condition.append(cond)
            elif type(dom) is list:
                cond, d = self._parseList(dom)
                data.extend(d)
                condition.append(cond)
            else:
                raise Core500Exception("Invalid domain part : {}, must be tuple or list".format(str(dom)))

        return ['(' + operator.join(condition) + ')', data]

    def _parseTuple(self, domain):
        if len(domain) != 3:
            raise Core500Exception("Invalid tuple for domain {}".format(domain))

        # Operateur de comparaison : domain[1]
        return domain[0] + ' ' + domain[1] + ' ' + "%s", [domain[2]]
