#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, getopt
import socket
import random
import request_pb2 as request
import response_pb2 as response
import communication
# from pathlib import Path

def setDefaultClient(message):
	message.command = ""
	message.protoVersion = "1.0"
	message.url = ""
	message.clientId = ""
	message.clientInfo = ""
	message.encoding = "utf-8"
	message.content = ""
	message.signature = ""

	return message

def createConection(IP, Port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		sock.connect((IP, int(Port)))
		print("Conexão Estabelecida")
	except ConnectionRefusedError:
		print("Conexão Recusada")
		exit(1)
	
	data = input("Para finalizar o programa, utilize 'SAIR'\nComando => ").upper()
	clientId = str(random.randint(1000,9999))
	while(data != "SAIR"):

		message = request.Request()
		message = setDefaultClient(message)

		message.command = data
		message.url = input("Url => ")
		message.clientId = clientId
		message.clientInfo = socket.gethostname().upper()
		
		if ((message.command == "GET") or (message.command == "DELETE")):
			message.content = "" 
		else:
			if(os.path.exists(message.url)):
				archive = open(message.url, 'r')
				message.content += archive.read()
				archive.close()
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
				print("\n######## RESPOSTA DO SERVIDOR ########")
				if message.command == "GET":
					print("STATUS:", responseFromServer.status)
					if("OK" in responseFromServer.status):
						print("CONTEUDO:")
						print(responseFromServer.content)
					else:
						print("Arquivo não encontrado")

				elif message.command == "POST":
					print("STATUS:", responseFromServer.status)
					if("OK" in responseFromServer.status):
						print("Arquivo {0} criado com sucesso!".format(responseFromServer.url))
					else:
						print("Falha ao criar o arquivo!")

				elif message.command == "DELETE":
					print("STATUS:", responseFromServer.status)
					if("OK" in responseFromServer.status):
						print("Arquivo {0} deletado com sucesso!".format(responseFromServer.url))
					else:
						print("Falha ao deletar o arquivo!")
				else:
					print("STATUS:", responseFromServer.status)
					print("Comando Desconhecido")
		print("\n######## NOVA REQUISIÇÃO ########")
		data = input("Para finalizar o programa, utilize 'SAIR'\nComando => ").upper()

def help():
	print("Usage => {0} -h -i/--ip <IP_Server> -p/--port <Port_Server>".format(sys.argv[0]))

def main(argv):
	IP = ''
	Port= 0

	try:
		opts, args = getopt.getopt(argv, "hi:p:",["ip=", "port="])
	except getopt.GetoptError:
		help()
		sys.exit(1)

	for opt, arg in opts:
		if opt == "-h":
			help()
			sys.exit()
		elif opt in ("-i", "--ip"):
			IP = arg
		elif opt in ("-p", "--port"):
			Port = arg

	if ((IP == '') or (Port == 0)):
		help()
		sys.exit(1)

	createConection(IP, Port)

if __name__ == '__main__':
	main(sys.argv[1:])

