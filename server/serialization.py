#coding: utf-8

class JsonSerializableObject(object):
    __serializable_fields = []

    def serialize_value(self, name, value):
        if isinstance(value, (str, unicode, int, long, float, bool, type(None))):
            return value
        elif isinstance(value, dict):
            return dict((key, self.serialize_value(key, val)) for key, val in value.iteritems())
        elif isinstance(value, (list, tuple)):
            return [self.serialize_value(None, val) for val in value]
        else:
            try:
                return value.to_dict()
            except AttributeError:
                return None

    def to_dict(self):
        serializable_fields = self.__serializable_fields or self.__dict__.keys()
        res = {}
        for field in serializable_fields:
            value = getattr(self, field)
            res[field] = self.serialize_value(field, value)
        return res

    def from_dict(self, d):
        serializable_fields = self.__serializable_fields or self.__dict__.keys()
        for field, value in d.iteritems():
            if field not in serializable_fields or not hasattr(self, field):
                continue

            if isinstance(value, list) and all([isinstance(list_value, dict) for list_value in value]):
                setattr(self, field, [self.parse_dict(field, list_value) for list_value in value])
            else:
                setattr(self, field, self.parse_dict(field, value))
        return self

    def parse_dict(self, name, value):
        return value
