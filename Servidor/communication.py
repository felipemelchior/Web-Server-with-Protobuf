#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import hmac
try:
    from google.protobuf.internal.encoder import _VarintEncoder
    from google.protobuf.internal.decoder import _DecodeVarint
except:
    print("Falha ao importar as bibliotecas\nTente: sudo pip3 google-cloud-storage")
from hashlib import sha256

def encodeVarint(data):
    packedData = []
    _VarintEncoder()(packedData.append, data, False)
    return b''.join(packedData)

def decodeVarint(data):
    return _DecodeVarint(data, 0)[0]

def sendMessage(socket, message):
	data = message.SerializeToString()
	size = encodeVarint(len(data))
	socket.sendall(size + data)

def recvMessage(socket, protoType):
    data = b''
    while True:
        try:
            data += socket.recv(1)
            size = decodeVarint(data)
            break
        except IndexError:
            pass

    data = socket.recv(size)
    message = protoType()
    message.ParseFromString(data)

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
