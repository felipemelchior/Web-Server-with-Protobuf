import os, sys, getopt
import socket
import random
from Mensagem import MessageCSV
from MessageServer import ServerCSV
import communication
import csv


def sendMessage(data, communication, clientId, sock, key):

	message = MessageCSV() # incializa o objeto MessageCSV
	message.setCommand(data)
	message.setClientId(clientId)
	urlArq = input("Url => ")
	message.setUrl(urlArq)

	infoClient = socket.gethostname().upper()
	message.setClientInfo(infoClient)

	if ((message.getCommand() == "GET") or (message.getCommand() == "DELETE")):
		contentMsg = ""
		message.setContent(contentMsg)
	elif(message.getCommand() == "POST"):
		try:
			arq = message.getUrl()

			archive = open('files/'+arq,  'r')
			conteudo = archive.read()

			message.setContent(conteudo)
			archive.close()

		except :
			print("Arquivo não localizado!")
			exit(1)
	else:
		pass

	signatureMsg = communication.hmacFromRequest(message, key)
	message.setSignature(signatureMsg)
	simb = ":"

	MessageEnd = message.getCommand() + simb  + message.getProtoVersion() + simb + message.getUrl() + simb + message.getClientId() + simb + message.getClientInfo() + simb + message.getEncoding() + simb + message.getSignature() + simb +  message.getContent()

	#print(MessageEnd)

	communication.sendMessage(sock, MessageEnd)
	return message # retorna o objeto

def getResponse(communication, message, sock,key):

	responseFromServer = communication.recvMessage(sock)

	if responseFromServer:
		signature = communication.hmacFromResponse(responseFromServer, key)
	
		if signature == responseFromServer.getSignature():
			print("\n######## RESPOSTA DO SERVIDOR ########")
			if message.getCommand() == "GET":
				print("STATUS:", responseFromServer.getStatus())
				if("OK" in responseFromServer.getStatus()):
					print("CONTEUDO:")
					print(responseFromServer.getContent())
					'''
					for i in responseFromServer.getContent():
						if(i != '\\'):
							print(i,end="")
						else:
							print()
					'''
					if(responseFromServer.getUrl() in ["/", ""]):
						archive = open("index.html", 'w+')
						archive.write(responseFromServer.getContent())					
					else:
						archive = open(responseFromServer.getUrl(), 'w+')
						archive.write(responseFromServer.getContent())
						'''
						with open(responseFromServer.getUrl()) as f:
            						for line in f:
								print(line)
						'''
				else:
					print("Arquivo não encontrado")

			elif message.getCommand()  == "POST":
				print("STATUS:", responseFromServer.getStatus())
				if("OK" in responseFromServer.getStatus()):
					print("Arquivo {0} criado com sucesso!".format(responseFromServer.getUrl()))
				else:
					print("Falha ao criar o arquivo!")
			elif message.getCommand()  == "DELETE":
				print("STATUS:", responseFromServer.getStatus())
				if("OK" in responseFromServer.getStatus()):
					print("Arquivo {0} deletado com sucesso!".format(responseFromServer.getUrl()))
				else:
					print("Falha ao deletar o arquivo!")
			else:
				print("STATUS:", responseFromServer.getStatus())
				print("Comando Desconhecido")
