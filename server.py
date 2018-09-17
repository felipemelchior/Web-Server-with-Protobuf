#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, getopt
import socket
import threading
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(threadName)s:%(message)s')

import request_pb2 as request
import response_pb2 as response
import communication
from pathlib import Path

def setDefaultServer(message):
	message.protoVersion = "1.0"
	message.serverInfo = "WebServer with Protobuf v1.0"
	message.encoding = "utf-8"

	return message

def getMethod(url):
	message = response.Response()
	archivePath = str(Path().absolute())
	archivePath += '/contents/'

	message = setDefaultServer(message)

	if url == '/':
		archivePath += 'index.html'
		
	else:
		if url[1] != '/':
			archivePath += "/" + url
		else:
			archivePath += url

	message.url = url

	try:
		archive = open(archivePath, 'r')
		message.content += archive.read()
		message.status = "OK - 200"
		logging.info(" GET {0}".format(url))

	except FileNotFoundError:
		message.status = "FAIL - 404"
		logging.info(" Archive not found")

	message.signature = communication.hmacFromResponse(message)

	return message

def postMethod(url, clientId, clientInfo, content):
	message = response.Response()
	archivePath = str(Path().absolute())
	archivePath += '/contents/'

	message = setDefaultServer(message)

	if url == '/':
		archivePath += 'index.html'
		
	else:
		if url[0] == '/':
			archivePath += str(''.join(url.split('/')))
		else:
			archivePath += url

	if os.path.exists(archivePath):
		logging.info(" POST {0}".format(url))
		logging.info(" POST in a existent file")
		message.status = "FAIL - 403"
	else:
		logging.info(" POST {0}".format(url))
		archivePathLock = archivePath + "." + clientId + clientInfo
		archive = open(archivePath, 'w')
		archiveLock = open(archivePathLock, 'w')

		archive.write(content)
		message.status = "OK - 200"
	message.url = url
	message.content = content
	message.signature = communication.hmacFromResponse(message)	

	return message
		

def deleteMethod(url, clientId, clientInfo):
	message = response.Response()
	archivePath = str(Path().absolute())
	archivePath += '/contents/'

	message = setDefaultServer(message)

	if url == '/':
		archivePath += 'index.html'
		
	else:
		if url[0] == '/':
			archivePath += str(''.join(url.split('/')))
		else:
			archivePath += url

	if os.path.exists(archivePath):
		logging.info(" DELETE {0}".format(url))
		archivePathLock = archivePath + "." + clientId + clientInfo
		
		if os.path.exists(archivePathLock):
				os.remove(archivePath)
				os.remove(archivePathLock)
				logging.info(" DELETE Sucessful".format(url))
				message.status = "OK - 200"
		else:	
			logging.info(" DELETE Unsucessful".format(url))
			message.status = "FAIL - 403"
		
	else:
		logging.info(" DELETE Unsucessful".format(url))
		message.status = "FAIL - 403"

	message.url = url
	message.content = ""
	message.signature = communication.hmacFromResponse(message)	

	return message

def unknownMethod():
	logging.info(" Unknown command")
	message = response.Response()
	message = setDefaultServer(message)
	message.status = "FAIL - 401"
	message.url = ""
	message.content = ""
	message.signature = communication.hmacFromResponse(message)	

	return message



def connected(client, addr):
	while True:
		message = communication.recvMessage(client, request.Request)

		if message:
			signature = communication.hmacFromRequest(message)
			if signature == message.signature:
				if message.command == "GET":
					response = getMethod(message.url)
					communication.sendMessage(client, response)

				elif message.command == "POST":
					response = postMethod(message.url, message.clientId, message.clientInfo, message.content)
					communication.sendMessage(client, response)
				
				elif message.command == "DELETE":
					response = deleteMethod(message.url, message.clientId, message.clientInfo)
					communication.sendMessage(client, response)
				else:
					response = unknownMethod()
					communication.sendMessage(client, response)
			client.close()	
			break	

def listenConnection(Port):
	try:
		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server.bind(('0.0.0.0', int(Port)))
		server.listen(10)

		logging.info(" WebServer running on port {0}".format(Port))

		while True:
			conn, addr = server.accept()
			threading.Thread(target=connected, args=(conn,addr)).start()

		server.close()

	except (KeyboardInterrupt, SystemExit):
		logging.info(" Finishing execution of WebServer...")
		pass


def help():
	print("Usage => {0} -h -p <Port>".format(sys.argv[0]))

def main(argv):
	Port= 0

	try:
		opts, args = getopt.getopt(argv, "hp:",["Port="])
	except getopt.GetoptError:
		help()
		sys.exit(1)

	for opt, arg in opts:
		if opt == "-h":
			help()
			sys.exit()
		elif opt in ("-p", "--Port"):
			Port = arg

	if Port == 0:
		help()
		sys.exit(1)

	listenConnection(Port)

if __name__ == '__main__':
	main(sys.argv[1:])

