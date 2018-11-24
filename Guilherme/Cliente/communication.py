#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import hmac
try:
	import bson
except:
	print("Falha ao importar as bibliotecas\nTente: sudo pip3 install bson")
from hashlib import sha256

def sendMessage(socket, message):
	socket.sendobj(message)

def recvMessage(socket):
	message = socket.recvobj()
	return message

def hmacFromRequest(message, key):
	body = message['command']
	body += message['protoVersion']
	body += message['url']
	body += message['clientId']
	body += message['clientInfo']
	body += message['encoding']
	body += message['content']
	body = body.encode('utf-8')

	signature = hmac.new(key.to_bytes(16, "big"), body).hexdigest()

	return str(signature)

def hmacFromResponse(message, key):
	body = message['status']
	body += message['protoVersion']
	body += message['url']
	body += message['serverInfo']
	body += message['encoding']
	body += message['content']
	body = body.encode('utf-8')

	signature = hmac.new(key.to_bytes(16, "big"), body).hexdigest()

	return str(signature)
