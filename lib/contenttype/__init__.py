import pkgutil
import importlib

Converter = dict()

for importer, modname, ispkg in pkgutil.iter_modules(__path__):
    if not ispkg:
        Converter[modname.replace('_', '/')] = importlib.import_module("lib.contenttype.{}".format(modname)).Converter
