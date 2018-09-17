#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, getopt
import socket
import random
import request_pb2 as request
import response_pb2 as response
import communication

def setDefaultClient(message):
	message.protoVersion = "1.0"
	message.encoding = "utf-8"
	message.content = ""

	return message

def createConection(IP, Port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		sock.connect((IP, int(Port)))
		print("Conexão Estabelecida")
	except ConnectionRefusedError:
		print("Conexão Recusada")
		exit(1)

	message = request.Request()
	message = setDefaultClient(message)

	message.command = input("Comando => ").upper()
	message.url = input("Url => ")
	message.clientId = str(random.randint(1000,9999))
	message.clientInfo = socket.gethostname().upper()
	
	if ((message.command == "GET") or (message.command == "DELETE")):
		message.content = "" 
	else:
		print("Para finalizar a mensagem use Ctrl+X")
		msg = input("Conteudo da Mensagem => ")
		while (msg != '\x18') :
			message.content += msg + "\r\n"
			msg = input()

	message.signature = communication.hmacFromRequest(message)

	communication.sendMessage(sock, message)

	responseFromServer = communication.recvMessage(sock, response.Response)

	if responseFromServer:
		signature = communication.hmacFromResponse(responseFromServer)
		if signature == responseFromServer.signature:
			if message.command == "GET":
				print(responseFromServer.status)
				print(responseFromServer.content)
				
			elif message.command == "POST":
				print(responseFromServer.status)
				if("OK" in responseFromServer.status):
					print("Arquivo {0} criado com sucesso!".format(responseFromServer.url))
				else:
					print("Falha ao criar o arquivo!")

			elif message.command == "DELETE":
				print(responseFromServer.status)
				if("OK" in responseFromServer.status):
					print("Arquivo {0} deletado com sucesso!".format(responseFromServer.url))
				else:
					print("Falha ao deletar o arquivo!")
			else:
				print(responseFromServer.status)
				print("Comando Desconhecido")
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

