import json
class Request:
    def __init__(self):
        self.command = ""
        self.protoVersion = "1.0"
        self.url = ""
        self.clientId = ""
        self.clientInfo = ""
        self.encoding = "utf-8"
        self.content = ""
        self.signature = ""

    def SerializeToString(self):
        data = self.__dict__
        serialized = json.dumps(data)
        return serialized.encode("utf8")

    def ParseFromString(self, data):
        data = data.decode()
        deserialized = json.loads(data)
        request = Request()
        request.command = deserialized['command']
        request.protoType = deserialized['protoVersion']
        request.url = deserialized['url']
        request.clientId = deserialized['clientId']
        request.clientInfo = deserialized['clientInfo']
        request.encoding = deserialized['encoding']
        request.content = deserialized['content']
        request.signature = deserialized['signature']
        return request
