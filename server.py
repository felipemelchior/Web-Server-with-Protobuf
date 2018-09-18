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
	'''
	Define os valores default da estrutura do protobuf
	Para evitar que faltem parametros no protobuf na hora de enviar ao cliente

	:param message: estrutura protobuf
	:return: estrutura protobuf com os valores definidos
	'''
	
	message.status = ""
	message.protoVersion = "1.0"
	message.url = ""
	message.serverInfo = "WebServer with Protobuf v1.0"
	message.encoding = "utf-8"
	message.content = ""
	message.signature = ""

	return message

def getMethod(url):
	'''
	Função que popula o protobuf enviando como conteudo, o arquivo que o cliente quer

	:param url: Url do arquivo desejado (ex: "index.html", "teste.txt")
	:return: Protobuf já pronto para o envio
	'''

	message = response.Response()
	archivePath = str(Path().absolute())
	archivePath += '/contents/'

	if not os.path.exists(archivePath):
		os.makedirs("contents")

	message = setDefaultServer(message)

	if url == '/':
		archivePath += 'index.html'
	
	else:
		if url[0] != '/':
			archivePath += "/" + url
		else:
			archivePath += url

	message.url = url

	logging.info(" GET {0}".format(url))

	try:
		archive = open(archivePath, 'r')
		message.content += archive.read()
		logging.info(" GET Sucessful")
		message.status = "OK - 200"
		archive.close()
	except FileNotFoundError:
		message.status = "FAIL - 404"
		logging.info(" Archive not found")

	message.signature = communication.hmacFromResponse(message)

	return message

def postMethod(url, clientId, clientInfo, content):
	'''
	Função que cria arquivos no servidor

	Cria um arquivo com o conteudo recebido do cliente
	Para manter a autoridade dos arquivos, também é criado um arquivo, com mesmo nome,
	porém, concatenado com a identificação e informação do cliente.

	:param url: Url onde o arquivo sera salvo
	:param clientId: Identificação do cliente
	:param clientInfo: Informação sobre o cliente, neste caso o hostname
	:return: Estrutura Protobuf já pronta para o envio
	'''

	message = response.Response()
	archivePath = str(Path().absolute())
	archivePath += '/contents/'

	if not os.path.exists(archivePath):
		os.makedirs("contents")

	message = setDefaultServer(message)

	if url == '/':
		archivePath += 'index.html'
		
	else:
		if url[0] == '/':
			archivePath += str(''.join(url.split('/')))
		else:
			archivePath += url

	logging.info(" POST {0}".format(url))

	if os.path.exists(archivePath):
		logging.info(" POST in a existent file")
		message.status = "FAIL - 403"
	else:
		archivePathLock = archivePath + "." + clientId + clientInfo
		archive = open(archivePath, 'w')
		archiveLock = open(archivePathLock, 'w')

		archive.write(content)
		logging.info(" POST Sucessful")
		message.status = "OK - 200"

		archive.close()
		archiveLock.close()
	message.url = url
	message.content = content
	message.signature = communication.hmacFromResponse(message)	

	return message
		
def deleteMethod(url, clientId, clientInfo):
	'''
	Função de remoção de arquivos

	Remove arquivos localizados no servidor
	Para segurança dos arquivos, faz o teste antes de remover
	O teste basicamente é uma busca pelo arquivo de lock (url + . + clientId + clientInfo)
	
	:param url: Url do arquivo que será removido
	:param clientId: Identificação do cliente
	:param clientInfo: Informação do cliente, neste caso é o hostname
	:return: Estrutura protobuf de resposta já pronta para envio
	'''

	message = response.Response()
	archivePath = str(Path().absolute())
	archivePath += '/contents/'

	if not os.path.exists(archivePath):
		os.makedirs("contents")

	message = setDefaultServer(message)
	if url == '/':
		archivePath += 'index.html'
		
	else:
		if url[0] == '/':
			archivePath += str(''.join(url.split('/')))
		else:
			archivePath += url

	logging.info(" DELETE {0}".format(url))

	if os.path.exists(archivePath):
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
	'''
	Função que é chamada quando o comando especificado pelo cliente não é conhecido
	Ex: "gets", "trace"
	'''

	logging.info(" Unknown command")
	message = response.Response()
	message = setDefaultServer(message)
	message.status = "FAIL - 401"
	message.signature = communication.hmacFromResponse(message)	

	return message

def connected(client, addr):
	'''
	Função que recebe a conexão

	Trata o protobuf recebido com base nos valores dele (ex: "GET /")

	:param client: Socket de conexão do cliente
	:param addr: Endereço IP do cliente
	'''

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

		while True:
			conn, addr = server.accept()
			threading.Thread(target=connected, args=(conn,addr)).start()

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