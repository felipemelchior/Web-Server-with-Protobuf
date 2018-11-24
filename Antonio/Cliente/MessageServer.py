class ServerCSV:

    def __init__(self):
        self.status = ""
        self.protoVersion = "1.0"
        self.url = ""
        self.serverId = ""
        self.serverInfo = "WebServer with Protobuf v1.0"
        self.encoding = "utf-8"
        self.signature = ""
        self.content = ""

    def setUrl(self, url):
        self.url = url

    def setServerId(self, serverId):
        self.serverId= serverId

    def setServerInfo(self, serverInfo):
        self.serverInfo = serverInfo

    def setContent(self, content):
        self.content = content

    def setProto(self, proto):
        self.protoVersion = proto

    def setEncod(self, cod):
        self.encoding = cod

    def setSignature(self, signature):
        self.signature = signature

    def setStatus(self, com):
        self.status = com

    def getStatus(self):
        return str(self.status)

    def getProtoVersion(self):
        return str(self.protoVersion)

    def getUrl(self):
        return str(self.url)

    def getServerId(self):
        return str(self.serverId)

    def getServerInfo(self):
        return str(self.serverInfo)

    def getEncoding(self):
        return (self.encoding)

    def getContent(self):
        return str(self.content)

    def getSignature(self):
        return str(self.signature)
