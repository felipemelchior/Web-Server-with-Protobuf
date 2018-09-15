#!/usr/bin/env python

import os, sys, getopt
import socket
import threading
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(threadName)s:%(message)s')

import request_pb2 as request
import response_pb2 as response
import communication

def connected(client, addr):
	while True:
		message = request.Request()
		buffer = communication.recvMessage(client)
		message.ParseFromString(buffer)

		if message:
			signature = communication.hmacFromMessage(message)
			print(signature)

def listenConnection(Port):
	try:
		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server.bind(('0.0.0.0', int(Port)))
		server.listen(10)

		logging.info("WebServer running on port {0}".format(Port))

		while True:
			conn, addr = server.accept()
			threading.Thread(target=connected, args=(conn,addr)).start()

		server.close()

	except (KeyboardInterrupt, SystemExit):
		logging.info("Finishing execution of WebServer...")
		pass


def help():
	print("Usage => {0} -h -p <Port>".format(sys.argv[0]))

def main(argv):
	Port= 0

	try:
		opts, args = getopt.getopt(argv, "hp:",["Port="])
	except getopt.GetoptError:
		help()
		sys.exit(1)

	for opt, arg in opts:
		if opt == "-h":
			help()
			sys.exit()
		elif opt in ("-p", "--Port"):
			Port = arg

	if Port == 0:
		help()
		sys.exit(1)

	listenConnection(Port)

if __name__ == '__main__':
	main(sys.argv[1:])

