#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, getopt
import socket
import random
import request_pb2 as request
import response_pb2 as response
import communication

def createConection(IP, Port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((IP, int(Port)))

	message = request.Request()

	message.command = input("Comando => ")
	message.protoVersion = "1.0"
	message.url = input("Url => ")
	message.clientId = str(random.randint(1000,9999))
	message.clientInfo = socket.gethostname()
	message.encoding = 'utf-8'
	
	if ((message.command == "GET") or (message.command == "DELETE")):
		message.content = "" 
	else:
		message.content = input("Conteudo da Mensagem => ")
	
	message.signature = communication.hmacFromMessage(message)

	communication.sendMessage(sock, message)

def help():
	print("Usage => {0} -h -i <IP> -p <Port>".format(sys.argv[0]))

def main(argv):
	IP = ''
	Port= 0

	try:
		opts, args = getopt.getopt(argv, "hi:p:",["IP=", "Port="])
	except getopt.GetoptError:
		help()
		sys.exit(1)

	for opt, arg in opts:
		if opt == "-h":
			help()
			sys.exit()
		elif opt in ("-i", "--IP"):
			IP = arg
		elif opt in ("-p", "--Port"):
			Port = arg

	if ((IP == '') or (Port == 0)):
		help()
		sys.exit(1)

	createConection(IP, Port)

if __name__ == '__main__':
	main(sys.argv[1:])

