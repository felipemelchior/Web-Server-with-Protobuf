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
from treatment.scrypt import key_exchange
from treatment.server import getMethod, postMethod, deleteMethod, unknownMethod

def connected(client, addr):
	'''
	Função que recebe a conexão

	Trata o protobuf recebido com base nos valores dele (ex: "GET /")

	:param client: Socket de conexão do cliente
	:param addr: Endereço IP e Porta do cliente
	'''

	key=key_exchange(client)

	while True:
		message = communication.recvMessage(client, request.Request)

		if message:
			signature = communication.hmacFromRequest(message, key)

			if signature == message.signature:
				if message.command == "GET":
					response = getMethod(message.url, message.clientId, message.clientInfo, key)
					communication.sendMessage(client, response)

				elif message.command == "POST":
					response = postMethod(message.url, message.clientId, message.clientInfo, message.content, key)
					communication.sendMessage(client, response)

				elif message.command == "DELETE":
					response = deleteMethod(message.url, message.clientId, message.clientInfo, key)
					communication.sendMessage(client, response)
				else:
					response = unknownMethod(key)
					communication.sendMessage(client, response)
	client.close()

def listenConnection(Ip, Port):
	'''
	Coloca o servidor para rodar, de fato

	Após, fica escutando a porta e quando chegar alguma conexão, cria um thread para o cliente
	e trata envia para a função que irá tratar a requisição

	:param Ip: Endereço Ip que o servidor irá rodar
	:param Port: Porta em que o servidor irá rodar
	'''

	try:
		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			server.bind((Ip, int(Port)))
			server.listen(10)
		except:
			logging.info(" Error on start server")

		logging.info(" WebServer running on port {0}".format(Port))

		try:
			while True:
				conn, addr = server.accept()
				logging.info(" New Connection from " + str(addr[0]) + " with port " + str(addr[1]))
				threading.Thread(target=connected, args=(conn,addr)).start()
		except:
			logging.info(" Port in use. Try start server again with another port")

		server.close()

	except (KeyboardInterrupt, SystemExit):
		logging.info(" Finishing execution of WebServer...")
		pass


def help():
	'''
	Exibe a ajuda

	No servidor, por padrão o parametro "-i/--ip" equivale ao localhost (127.0.0.1)
	'''

	print("WebServer with Protobuf - Server\n")
	print("Métodos disponíveis:\n-> GET - Faz o pedido de um arquivo a um servidor")
	print("-> POST - Envia um arquivo para o servidor")
	print("-> DELETE - Exclui um arquivo do servidor, apenas o dono do arquivo consegue deletar este arquivo")
	print("Uso => python3 {0} -h -i/--ip <IP_Server> -p/--port <Port_Server>".format(sys.argv[0]))
	print("\n\nParametros\n-h\t\tExibe a ajuda")
	print("-i/--ip\t\tParametro que define o IP do servidor")
	print("-p/--port\tParametro que define a Porta em o que o servidor está rodando")

def main(argv):
	'''
	Função principal que define os parametros do programa e também faz a chamada
	da função que colocará o servidor para funcionar

	:param argv: lista de parametros
	'''

	Ip = '127.0.0.1'
	Port= 0

	try:
		opts, args = getopt.getopt(argv, "hi:p:",["ip=","port="])
	except getopt.GetoptError:
		help()
		sys.exit(1)

	for opt, arg in opts:
		if opt == "-h":
			help()
			sys.exit()
		elif opt in ("-i", "--ip"):
			Ip = arg
		elif opt in ("-p", "--port"):
			Port = arg

	if Port == 0:
		help()
		sys.exit(1)

	listenConnection(Ip, Port)

if __name__ == '__main__':
	'''
	Inicio do programa, apenas faz a chamada da função principal
	'''

	main(sys.argv[1:])
