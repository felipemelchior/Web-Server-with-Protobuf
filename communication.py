#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket, struct
from hashlib import sha256

def readSocktSize(socket, size):
    buffer = ''

    while size > 0:
        data = socket.recv(size)
        buffer += str(data)
        size -= len(data)

    return buffer

def sendMessage(socket, message):
	data = message.SerializeToString()
	size = struct.pack('>L', len(data))
	socket.sendall(size + data)

def recvMessage(socket):
    sizeBuffer = readSocktSize(socket, 4)
    sizeMessage = struct.unpack('>L', sizeBuffer.encode('utf-8'))[0]
    data = readSocktSize(socket, sizeMessage)

    return data    

def hmacFromMessage(message):
    body = message.command
    body += message.protoVersion
    body += message.url
    body += message.clientId
    body += message.clientInfo
    body += message.encoding
    body += message.content
    body = body.encode('utf-8')

    key = "key"
    trans_5C = "".join(chr(x ^ 0x5c) for x in range(256))
    trans_36 = "".join(chr(x ^ 0x36) for x in range(256))
    blocksize = sha256().block_size

    if(len(key) > blocksize):
        key = sha256(key).digest()
    key += chr(0) * (blocksize - len(key))
    o_key_pad = key.translate(trans_5C).encode('utf-8')
    i_key_pad = key.translate(trans_36).encode('utf-8')

    signature = sha256(o_key_pad + sha256(i_key_pad + body).digest()).hexdigest()

    return str(signature)