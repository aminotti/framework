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

from flask import current_app
from .controller import Controller
from .context import models
from .module import SmartManagement


ctl = Controller()


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
