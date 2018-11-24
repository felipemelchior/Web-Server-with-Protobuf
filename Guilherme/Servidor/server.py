#!/usr/bin/env python
# -*- coding: utf-8 -*-

import getopt
import logging
import os
import socket
import sys
import threading
from pathlib import Path

import communication
from treatment.scrypt import key_exchange
from treatment.server import (clearRules, deleteMethod, getMethod, postMethod,
                              synFlood, unknownMethod)

try:
    import bson
except:
    print("Falha ao importar as bibliotecas\nTente: sudo pip3 install bson")

logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(threadName)s:%(message)s')


def connected(client, addr):
	'''
	Função que recebe a conexão

	Trata o protobuf recebido com base nos valores dele (ex: "GET /")

	:param client: Socket de conexão do cliente
	:param addr: Endereço IP e Porta do cliente
	'''

	key=key_exchange(client)

	while True:
		message = communication.recvMessage(client)
		if message:
			signature = communication.hmacFromRequest(message, key)
			print('sig = {0}'.format(signature))
			print('message = {0}'.format(message['signature']))

			if signature == message['signature']:
				print('aqui')
				if message['command'] == "GET":
					response = getMethod(message['url'], message['clientId'], message['clientInfo'], key)
					communication.sendMessage(client, response)

				elif message['command'] == "POST":
					response = postMethod(message['url'], message['clientId'], message['clientInfo'], message['content'], key)
					communication.sendMessage(client, response)

				elif message['command'] == "DELETE":
					response = deleteMethod(message['url'], message['clientId'], message['clientInfo'], key)
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
		bson.patch_socket()
		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			server.bind((Ip, int(Port)))
			server.listen(10)
		except:
			logging.info(" Error on start server")

		logging.info(" WebServer running on port {0}".format(Port))

		threads = []

		try:
			while True:
				conn, addr = server.accept()
				logging.info(" New Connection from " + str(addr[0]) + " with port " + str(addr[1]))

				aux = threading.Thread(target=connected, args=(conn,addr))
				aux.setDaemon(True)
				aux.start()
				threads.append(aux)
		except:
			if(os.getuid() == 0):
				clearRules()
			logging.info(" Ending the server execution")

		server.close()

	except (KeyboardInterrupt, SystemExit):
		if(os.getuid() == 0):
			clearRules()
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

	if(sys.platform == 'linux'):
		if(os.getuid() == 0):
			synFlood()
		else:
			logging.info(" To prevent Syn Flood Attack, run the server with sudo")

	listenConnection(Ip, Port)

if __name__ == '__main__':
	'''
	Inicio do programa, apenas faz a chamada da função principal
	'''

	main(sys.argv[1:])
