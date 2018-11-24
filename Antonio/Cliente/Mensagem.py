class MessageCSV:

    def __init__(self):
        self.command = ""
        self.protoVersion = "1.0"
        self.url = ""
        self.clientId = ""
        self.clientInfo = ""
        self.encoding = "utf-8"
        self.signature = ""
        self.content = ""

    def setUrl(self, url):
        self.url = url
    def setClientId(self, clientId):
        self.clientId = clientId

    def setClientInfo(self, clientInfo):
        self.clientInfo = clientInfo

    def setContent(self, content):
        self.content = content

    def setSignature(self, signature):
        self.signature = signature

    def setCommand(self, com):
        self.command = com

    def getCommand(self):
        return str(self.command)

    def setProto(self, proto):
        self.protoVersion = proto

    def getProtoVersion(self):
        return str(self.protoVersion)

    def getUrl(self):
        return str(self.url)

    def getClientId(self):
        return str(self.clientId)

    def getClientInfo(self):
        return str(self.clientInfo)

    def setEncod(self, cod):
        self.encoding = cod
        
    def getEncoding(self):
        return (self.encoding)

    def getContent(self):
        return str(self.content)

    def getSignature(self):
        return str(self.signature)
