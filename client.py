#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, getopt
import socket
import random
import request_pb2 as request
import response_pb2 as response
import communication

def setDefaultClient(message):
	'''
	Define os valores default da estrutura do protobuf
	Para evitar que faltem parametros no protobuf na hora de enviar ao servidor

	:param message: estrutura protobuf
	:return: estrutura protobuf com os valores definidos
	'''

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
	'''
	Cria a conexao com o servidor e popula o protobuf de acordo com o cliente atual
	Roda a comunicação cliente-servidor enquanto o cliente quiser (até digitar "SAIR")

	Envia o protobuf de requisição populado e recebe um protobuf de resposta já populado também
	Imprime na tela, os pedidos da requisição e a resposta de acordo com o protobuf de resposta

	:param IP: IP do servidor
	:Port: Porta em que o servidor está rodando
	'''

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
	'''
	Exibe a ajuda
	'''
	
	print("WebServer with Protobuf - Cliente\n")
	print("Métodos disponíveis:\n-> GET - Faz o pedido de um arquivo a um servidor")
	print("-> POST - Envia um arquivo para o servidor")
	print("-> DELETE - Exclui um arquivo do servidor, apenas o dono do arquivo consegue deletar este arquivo")
	print("Uso => python3 {0} -h -i/--ip <IP_Server> -p/--port <Port_Server>".format(sys.argv[0]))
	print("\n\nParametros\n-h\t\tExibe a ajuda")
	print("-i/--ip\t\tParametro que define o IP do servidor")
	print("-p/--port\tParametro que define a Porta em o que o servidor está rodando")

def main(argv):
	'''
	Funcao principal, onde sao definidos os parametros e onde é feita a chamada da função que inicia o programa

	:param argv: lista de argumentos passados na execução
	'''

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
	'''
	Inicio do programa e chamada da funcoa principal
	'''
	main(sys.argv[1:])

