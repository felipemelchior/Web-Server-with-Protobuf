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

def sendMessage(data, communication, clientId, sock):
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
    return message

def getRespose(communication, message, sock):
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
