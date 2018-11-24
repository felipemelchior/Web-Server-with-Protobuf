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
from Mensagem import MessageCSV
from MessageServer import ServerCSV

def encodeVarint(data):
    packedData = []
    _VarintEncoder()(packedData.append, data, False)
    return b''.join(packedData)

def decodeVarint(data):
    return _DecodeVarint(data, 0)[0]

def sendMessage(socket, message):
    data = str.encode(message) #.SerializeToString()
    size = encodeVarint(len(data))
    #print(type(size))
    socket.sendall(size + data)

def recvMessage(socket):
    data = b''
    while True:
        try:
            data += socket.recv(1)
            size = decodeVarint(data)
            break
        except IndexError:
            pass

    data = socket.recv(size)
    data = str(data)

    status, proto, url, serId, serInfo, encod, signt, conteu = data.split(':')

    message =ServerCSV()
    status = status[2:]
    #print(comand)
    message.setStatus(status)
    message.setProto(proto)
    message.setUrl(url)
    message.setServerId(serId)
    message.setServerInfo(serInfo)
    message.setEncod(encod)
    message.setSignature(signt)
    message.setContent(conteu)
    #print(comand)
    return message

def hmacFromRequest(message, key):
    body = message.getCommand()
    body += message.getProtoVersion()
    body += message.getUrl()
    body += message.getClientId()
    body += message.getClientInfo()
    body += message.getEncoding()
    #body += message.getContent()
    body = body.encode('utf-8')

    signature = hmac.new(key.to_bytes(16, "big"), body).hexdigest()

    return str(signature)

def hmacFromResponse(message, key):
    body = message.getStatus()
    body += message.getProtoVersion()
    body += message.getUrl()
    body += message.getServerId()
    body += message.getServerInfo()
    body += message.getEncoding()
    #body += message.content
    body = body.encode('utf-8')

    signature = hmac.new(key.to_bytes(16, "big"), body).hexdigest()

    return str(signature)
