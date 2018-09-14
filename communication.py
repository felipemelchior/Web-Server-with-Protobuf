#!/usr/bin/env python

import socket
import hashlib
import hmac

def sendMessage(socket, message):
	data.message.SerializeToString()
	size = encode_varint(len(data))
	socket.sendall(size + data)

def hmacFromMessage(message):
    body = message.command
    body += message.protoVersion
    body += message.url
    body += message.clientId
    body += message.clientInfo
    body += message.encoding
    body += message.content
    signature = hmac.new(b'WebServerNonSecure', body.encode('utf-8'), hashlib.sha256).hexdigest()
    print(signature)
    return signature