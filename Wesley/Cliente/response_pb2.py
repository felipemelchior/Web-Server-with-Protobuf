import json
class Response:
    def __init__(self):
        self.status = ""
        self.protoVersion = "1.0"
        self.url = ""
        self.serverInfo = "WebServer with Protobuf v1.0"
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
        respose = Response()
        respose.status = deserialized['status']
        respose.protoType = deserialized['protoVersion']
        respose.url = deserialized['url']
        respose.serverInfo = deserialized['serverInfo']
        respose.encoding = deserialized['encoding']
        respose.content = deserialized['content']
        respose.signature = deserialized['signature']
        return respose
