class Converter(object):
    @classmethod
    def toDict(cls, data):
        raise NotImplementedError

    @classmethod
    def fromDict(cls, dico):
        raise NotImplementedError
