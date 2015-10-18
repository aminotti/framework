import re
import datetime
import dateutil.parser

from . import regex


class Parser(object):
    """ Tools compliant with :rfc:`3339` to play with dates and times."""
    @staticmethod
    def dateFromString(string):
        """
        Convert a date, datetime or time from string to python object.

        :param str string: A string in :rfc:`3339` format.
        :rtype: :py:class:`datetime.date`, :py:class:`datetime.datetime` or :py:class:`datetime.time`.
        """
        try:
            if regex.RFC3339.date.match(string):
                return datetime.datetime.strptime(string, "%Y-%m-%d").date()
            elif regex.RFC3339.datetime.match(string):
                return dateutil.parser.parse(string).astimezone(dateutil.tz.tzutc())
            elif regex.RFC3339.time.match(string):
                return dateutil.parser.parse(string).time()
        except:
            pass
        return string
