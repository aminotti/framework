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


def depends(*dependencies):
    """ For compute field """
    def wrap(f):
        def wrapper_f(*args):
            # Return None if dependencies are not set
            for attr in dependencies:
                if not args[0]._fields[attr]:
                    return None
            r = f(*args)
            return r
        # Register attribute dependance
        setattr(wrapper_f, '_depends', *dependencies)
        return wrapper_f
    return wrap


def onchange(*dependencies):
    """ Workflow trigger on field update """
    def wrap(f):
        def wrapper_f(*args):
            # Run method if one of the TODO ameliorer commentaire
            for attr in dependencies:
                if not args[0]._fields[attr]:
                    return None
            f(*args)
        # Register attribute dependance
        setattr(wrapper_f, '_onchange', *dependencies)
