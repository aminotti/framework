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

import sys
from termcolor import colored
import inspect


def debug(string):
    """ Print debug infos to console.

    :param str string: message to print.
    """
    print '[' + colored('DEBUG', 'blue') + ']', string


def error(string):
    """ Print error message to stderr.

    :param str string: message to print.
    """
    print >> sys.stderr, '[' + colored('ERROR', 'red') + ']', string


def info(string):
    """ Print information message to console.

    :param str string: message to print.
    """
    print '[' + colored('INFO', 'green') + ']', string
