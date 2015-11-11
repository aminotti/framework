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
import io
from flask import current_app
from app.config import conf


class Binary(object):
    base_url = "/binaries"

    def __init__(self, ressource, name, mimetype, extension, stream=None, uuid=None):
        """ Create new binary object.

        :param str ressource: Name of the ressource
        :param str attribute: The name of the ressource's field which use these stream as value.
        :param str extension: extension use in filename of the stream
        :param io.BytesIO stream: The steam of binary data.
        :parma str uuid: UUID use as filename when storing on file system
        """
        self.ressource = ressource
        self.attribute = name
        self.mimetype = mimetype
        self.extension = extension
        self.stream = stream
        self.uuid = uuid

    def save(self):
        """ Save a binary to file on File system. """

        directory = os.path.join(conf.data_dir, current_app.tenant, self.ressource, self.attribute)
        path = os.path.join(directory, self.uuid + "." + self.extension)
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(path, 'wb') as outfile:
            outfile.write(self.stream.getvalue())

    def loadStreamFromDB(self, identifiers):
        """ Load extra infos for stream from Database.

        :param list identifiers: List of identifiers of the ressource.
        """
        self.identifiers = identifiers

    def loadStreamFromFS(self, identifiers):
        """ Load a file to self.stream from File system.

        :param list identifiers: List of identifiers of the ressource.
        """
        self.identifiers = identifiers

        with open(self._getPath(), "rb") as infile:
            self.stream = io.BytesIO(infile.read())

    def removeStreamFromFS(self):
        """ Remove the stream from File system. """
        path = self._getPath()

        if os.path.isfile(path):
            os.unlink(path)

    def getURL(self):
        """ Retrieve URL. loadStreamFromFS() or loadStreamFromDB() have to be called first."""
        identifiers = "/".join(self.identifiers)
        return "{}/{}/{}/{}.{}".format(self.base_url, self.ressource, identifiers, self.attribute, self.extension)

    def _getPath(self):
        return os.path.join(conf.data_dir, current_app.tenant, self.ressource, self.attribute, self.uuid + "." + self.extension)
