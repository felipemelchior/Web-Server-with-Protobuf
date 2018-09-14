#!/usr/bin/env python

import os, sys, getopt
import socket
import threading
import random
import request_pb2 as request
import response_pb2 as response

def sendMessage(socket, message):
	data.message.SerializeToString()
	size = encode_varint(len(data))
	socket.sendall(size + data)

def createConection(IP, Port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((IP, int(Port)))

	message = request.Request()

	message.command = upper(input("Comando => "))
	message.url = input("Url => ")
	message.clientID = random.randint(1000,9999)
	message.clientInfo = socket.gethostname()
	
	if ((message.command == "GET") or (message.command == "DELETE")):
		message.content = "" 
	else:
		message.content = input("Conteudo da Mensagem => ")
	

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

	print(opts)

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

	print(IP, Port)

	createConection(IP, Port)

if __name__ == '__main__':
	main(sys.argv[1:])

