import json
import decimal
import datetime

from ..exceptions import *
from ..rfc3339 import Parser
import lib.orm.base


class Converter(object):
    @classmethod
    def toDict(cls, data):
        try:
            ret = json.loads(data, object_hook=cls._json_python)
        except Exception as e:
            raise Core400Exception("<MalformedJSON> " + str(e))
        return ret

    @classmethod
    def fromDict(cls, data):
        try:
            if type(data) is list and len(data) == 1:
                data = data[0]
            ret = json.dumps(data, sort_keys=True, cls=PythonJsonEncoder, ensure_ascii=False)
        except Exception as e:
            raise Core400Exception("<MalformedJSON> " + str(e))
        return ret

    @classmethod
    def _json_python(cls, json_dict):
        """ Converti en type python les type pas pris en charge en JSON """
        for (key, value) in json_dict.items():
            json_dict[key] = Parser.dateFromString(value)
        return json_dict


class PythonJsonEncoder(json.JSONEncoder):
    def default(self, data):
        if isinstance(data, decimal.Decimal):
            return float(data)
        elif isinstance(data, datetime.datetime):
            return data.strftime("%Y-%m-%dT%H:%MZ")
        elif isinstance(data, datetime.date):
            return data.strftime("%Y-%m-%d")
        elif isinstance(data, datetime.timedelta):
            return (datetime.datetime.min + data).time().strftime("%H:%M")
        elif isinstance(data, datetime.time):
            return data.strftime("%H:%M")
        elif isinstance(data, lib.orm.base.Mapper):
            return vars(data)
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, data)
