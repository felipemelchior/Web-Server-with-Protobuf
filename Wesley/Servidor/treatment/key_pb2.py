import json
class Prime_key:
    def __init__(self):
        self.base = 1
        self.public = 1

    def SerializeToString(self):
        data = self.__dict__
        serialized = json.dumps(data)
        return serialized.encode("utf8")

    def ParseFromString(self, data):
        data = data.decode()
        deserialized = json.loads(data)
        respose = Prime_key()
        respose.base = deserialized['base']
        respose.public = deserialized['public']
        return respose

class Public_key:
    def __init__(self):
        self.key = 1

    def SerializeToString(self):
        data = self.__dict__
        serialized = json.dumps(data)
        return serialized.encode("utf8")

    def ParseFromString(self, data):
        data = data.decode()
        deserialized = json.loads(data)
        respose = Public_key()
        respose.key = deserialized['key']
        return respose
