import json


class JsonEncodable(object):
    """
    any subclasses of this class can be encoded to json
    """
    def jsonDefault(self):
        return self.__dict__

    def toJSON(self):
        return json.dumps(self.jsonDefault(), cls=JsonifiableEncoder,
                          ensure_ascii=False).encode('utf-8')


class JsonDecodable(object):
    """
    any subclasses of this class can be decode-constructed from json
    """
    @classmethod
    def fromJSON(cls, jsonData):
        raise NotImplementedError


class Jsonifiable(JsonEncodable, JsonDecodable):
    """
    any subclasses of this class should be both decodable and encodable from/to json
    """
    pass


class JsonifiableEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, JsonEncodable):
            return obj.jsonDefault()
        else:
            return super().default(obj)
