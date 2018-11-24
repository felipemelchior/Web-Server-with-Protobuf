#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, getopt
import socket
import random
import communication
from treatment.ccrypt import key_exchange
from treatment.client import getResponse, sendMessage
from Mensagem import MessageCSV
from MessageServer import ServerCSV

def helpMessage():
	directory = os.listdir('files/')
	print("\nComandos disponíveis:\n\n\tGET - Recebe um arquivo do Servidor\n\tPOST - Envia um arquivo existente para o Servidor\n\tDELETE - Exclui um arquivo de sua autoria do servidor\n\nPara finalizar o programa, utilize 'SAIR'")
	print('\nArquivos existentes a enviar: \n',directory)

def createConection(IP, Port):
	'''
	Cria a conexao com o servidor e popula a mensagem CSV de acordo com o cliente atual
	Roda a comunicação cliente-servidor enquanto o cliente quiser (até digitar "SAIR")

	Envia a mesnagem CSV de requisição populado e recebe uma mesangem CSV de resposta já populado também
	Imprime na tela, os pedidos da requisição e a resposta de acordo com a mesnagem CSV de resposta

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

	helpMessage()
	data = input("\nComando => ").upper()
	clientId = str(random.randint(1000,9999))

	key=key_exchange(sock)

	while(data != "SAIR"):
		message = sendMessage(data, communication, clientId, sock, key)
		getResponse(communication, message, sock, key)

		print("\n######## NOVA REQUISIÇÃO ########")
		helpMessage()
		data = input("\nComando => ").upper()

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
	Inicio do programa e chamada da funcao principal
	'''
	main(sys.argv[1:])
