#!/usr/bin/env python
# -*- coding: utf-8 -*-

import getopt
import os
import random
import socket
import sys

import communication


def setDefaultClient(message):
	'''
	Define os valores default da estrutura do protobuf
	Para evitar que faltem parametros no protobuf na hora de enviar ao servidor

	:param message: estrutura protobuf
	:return: estrutura protobuf com os valores definidos
	'''
	message['command'] = ""
	message['protoVersion'] = "1.0"
	message['url'] = ""
	message['clientId'] = ""
	message['clientInfo'] = ""
	message['encoding'] = "utf-8"
	message['content'] = ""
	message['signature'] = ""

	return message

def sendMessage(data, communication, clientId, sock, key):
	message = {}
	message = setDefaultClient(message)

	message['command'] = data
	message['url'] = input("Url => ")
	message['clientId'] = clientId
	message['clientInfo'] = socket.gethostname().upper()

	if ((message['command'] == "GET") or (message['command'] == "DELETE")):
		message['content'] = ""
	elif(message['command'] == "POST"):
		try:
			archive = open(message['url'], 'r')
			message['content'] += archive.read()
			archive.close()
		except:
			print("Arquivo não localizado!")
			exit(1)

	message['signature'] = communication.hmacFromRequest(message, key)
	communication.sendMessage(sock, message)
	return message

def getResponse(communication, message, sock,key):
	responseFromServer = communication.recvMessage(sock)

	if responseFromServer:

		signature = communication.hmacFromResponse(responseFromServer, key)

		if signature == responseFromServer['signature']:
			print("\n######## RESPOSTA DO SERVIDOR ########")
			if message['command'] == "GET":
				print("STATUS:", responseFromServer['status'])
				if("OK" in responseFromServer['status']):
					print("CONTEUDO:")
					print(responseFromServer['content'])

					if not os.path.exists("contents"):
						os.makedirs("contents")

					if(responseFromServer['url'] in ["/", ""]):
						archive = open("./contents/index.html", 'w')
						archive.write(responseFromServer['content'])
						archive.close()
					else:
						archive = open("./contents/{}".format(responseFromServer['url'].split('/')[-1]), 'w')
						archive.write(responseFromServer['content'])
						archive.close()

				else:
					print("Arquivo não encontrado")

			elif message['command'] == "POST":
				print("STATUS:", responseFromServer['status'])
				if("OK" in responseFromServer['status']):
					print("Arquivo {0} criado com sucesso!".format(responseFromServer['url']))
				else:
					print("Falha ao criar o arquivo!")

			elif message['command'] == "DELETE":
				print("STATUS:", responseFromServer['status'])
				if("OK" in responseFromServer['status']):
					print("Arquivo {0} deletado com sucesso!".format(responseFromServer['url']))
				else:
					print("Falha ao deletar o arquivo!")
			else:
				print("STATUS:", responseFromServer['status'])
				print("Comando Desconhecido")
