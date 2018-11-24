#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import hmac
from hashlib import sha256

def sendMessage(socket, message):
    data = message.SerializeToString()
    size = len(data).to_bytes(16, "big")
    socket.sendall(size + data)

def recvMessage(socket, protoType):
    data = b''
    size = int.from_bytes(socket.recv(16), "big")
    data = socket.recv(size)
    message = protoType()
    message = message.ParseFromString(data)

    return message

def hmacFromRequest(message, key):
    body = message.command
    body += message.protoVersion
    body += message.url
    body += message.clientId
    body += message.clientInfo
    body += message.encoding
    body += message.content
    body = body.encode('utf-8')

    signature = hmac.new(key.to_bytes(16, "big"), body).hexdigest()

    return str(signature)

def hmacFromResponse(message, key):
    body = message.status
    body += message.protoVersion
    body += message.url
    body += message.serverInfo
    body += message.encoding
    body += message.content
    body = body.encode('utf-8')

    signature = hmac.new(key.to_bytes(16, "big"), body).hexdigest()

    return str(signature)
