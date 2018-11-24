import os, sys, getopt
import socket
import threading
import logging
import communication
from pathlib import Path
from Mensagem import MessageCSV
from MessageServer import ServerCSV
import csv

def getMethod(url, clientId, clientInfo, key):
	'''
	Função que popula a mensagem  enviando como conteudo, o arquivo que o cliente quer

	:param url: Url do arquivo desejado (ex: "index.html", "teste.txt")
	:return: Mensagem CSVjá pronta para o envio
	'''

	message = ServerCSV()
	archivePath = str(Path().absolute())
	archivePath += '/contents/'

	if not os.path.exists(archivePath):
		os.makedirs("contents")

	if(url in ['/','']):
		archivePath += 'index.html'

	else:
		archivePath += clientInfo + "/"

		if url[0] != '/':
			archivePath += "/" + url
		else:
			archivePath += url

	message.setUrl( url)

	logging.info(" GET {0}".format(url))

	try:
		archive = open(archivePath, 'r')
		nameFile = archive.name
		conteudo = archive.read()
		message.setContent(conteudo)
		logging.info(" GET Sucessful")
		message.setStatus("OK - 200")
		message.setUrl(url)
		archive.close()
	except FileNotFoundError:
		message.setStatus("FAIL - 404")
		logging.info(" Archive not found")

	signature = communication.hmacFromResponse(message, key)
	message.setSignature(signature)

	simb = ":"

	MessageEnd = message.getStatus() + simb  + message.getProtoVersion() + simb + message.getUrl() + simb + message.getServerId() + simb + message.getServerInfo() + simb + message.getEncoding() + simb + message.getSignature() + simb +  message.getContent()

	#print(MessageEnd)

	return MessageEnd

def postMethod(url, clientId, clientInfo, content, key):
	'''
	Função que cria arquivos no servidor

	Cria um arquivo com o conteudo recebido do cliente
	Para manter a autoridade dos arquivos, também é criado um arquivo, com mesmo nome,
	porém, concatenado com a identificação e informação do cliente.

	:param url: Url onde o arquivo sera salvo
	:param clientId: Identificação do cliente
	:param clientInfo: Informação sobre o cliente, neste caso o hostname
	:return: Estrutura Mensagem CSV já pronta para o envio
	'''

	message = ServerCSV()

	archivePath = str(Path().absolute())
	archivePath += '/contents/'

	if not os.path.exists(archivePath):
		os.makedirs("contents")

	archivePath += clientInfo + "/"

	if not os.path.exists(archivePath):
		os.makedirs("contents/" + clientInfo)

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
		message.setStatus("FAIL - 403")
	else:
		archive = open(archivePath, 'w+')
		archive.write(content)
		logging.info(" POST Sucessful")
		message.setStatus("OK - 200")
		'''
		with open(archivePath, 'w', newline='') as f:
			writer = csv.writer(f)
			writer.writerows(someiterable)
		'''
		archive.close()

	message.setUrl(url)
	message.setContent(content)
	signature = communication.hmacFromResponse(message, key)
	message.setSignature(signature)
	simb = ":"

	MessageEnd = message.getStatus() + simb  + message.getProtoVersion() + simb + message.getUrl() + simb + message.getServerId() + simb + message.getServerInfo() + simb + message.getEncoding() + simb + message.getSignature() + simb +  message.getContent()

	return MessageEnd

def deleteMethod(url, clientId, clientInfo, key):
	'''
	Função de remoção de arquivos

	Remove arquivos localizados no servidor
	Para segurança dos arquivos, faz o teste antes de remover
	O teste basicamente é uma busca pelo arquivo de lock (url + . + clientId + clientInfo)

	:param url: Url do arquivo que será removido
	:param clientId: Identificação do cliente
	:param clientInfo: Informação do cliente, neste caso é o hostname
	:return: Estrutura Mensagem CSC de resposta já pronta para envio
	'''

	message = ServerCSV()
	archivePath = str(Path().absolute())
	archivePath += '/contents/'

	if not os.path.exists(archivePath):
		os.makedirs("contents")

	archivePath += clientInfo + "/"

	if url == '/':
		archivePath += 'index.html'

	else:
		if url[0] == '/':
			archivePath += str(''.join(url.split('/')))
		else:
			archivePath += url

	logging.info(" DELETE {0}".format(url))

	if os.path.exists(archivePath):
		os.remove(archivePath)
		logging.info(" DELETE Sucessful".format(url))
		message.setStatus("OK - 200")
	else:
		logging.info(" DELETE Unsucessful".format(url))
		message.setStatus("FAIL - 403")

	message.setUrl(url)
	message.setContent("")
	signature = communication.hmacFromResponse(message, key)
	message.setSignature(signature)
	simb = ":"

	MessageEnd = message.getStatus() + simb  + message.getProtoVersion() + simb + message.getUrl() + simb + message.getServerId() + simb + message.getServerInfo() + simb + message.getEncoding() + simb + message.getSignature() + simb +  message.getContent()

	return MessageEnd

def unknownMethod(key):
	'''
	Função que é chamada quando o comando especificado pelo cliente não é conhecido
	Ex: "gets", "trace"
	'''

	logging.info(" Unknown command")
	message = ServerCSV()
	message.setStatus("FAIL - 401")
	signature = communication.hmacFromResponse(message, key)
	message.setSignature(signature)
	simb = ":"

	MessageEnd = message.getStatus() + simb  + message.getProtoVersion() + simb + message.getUrl() + simb + message.getServerId() + simb + message.getServerInfo() + simb + message.getEncoding() + simb + message.getSignature() + simb +  message.getContent()

	return MessageEnd
