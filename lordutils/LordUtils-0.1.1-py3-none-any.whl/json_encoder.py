from json import JSONEncoder
import json


class JEncoder(JSONEncoder):

    def default(self, obj):
        if hasattr(obj, 'to_json'):
            return obj.to_json()
        if hasattr(obj, 'to_dict'):
            return obj.to_dict()
        if hasattr(obj, '__list__'):
            return obj.__list__
        if hasattr(obj, '__dict__'):
            return obj.__dict__
        return JSONEncoder.default(self, obj)

    @staticmethod
    def to_json_string(value):
        return json.dumps(value, cls=JEncoder, indent=4)

