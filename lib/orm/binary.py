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
from flask import current_app
from app.config import conf


class Binary(object):
    base_url = "/binary"

    def __init__(self, name=None, mimetype=None, extension=None, stream=None):
        """ Create new binary object.

        ;param str name: The name of the ressource's field which use these stream as value.
        ;param str extension: extension use in filename of the stream
        ;param str stream: The steam of binary data.
        """
        self.name = name
        self.mimetype = mimetype
        self.extension = extension
        self.stream = stream

    def save(self, ressource, identifiers):
        directory = os.path.join(conf.data_dir, current_app.tenant, ressource, self.name)
        path = os.path.join(directory, identifiers + "." + self.extension)

        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(path, 'wb') as outfile:
            outfile.write(self.stream.getvalue())

    def getURL(self, tenant, identifiers):
        # TODO get relative URL
        pass
