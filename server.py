#!/usr/bin/env python

import os, sys, getopt
import socket
import threading
import request_pb2 as request
import response_pb2 as response

def listenConnection(Port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind(('0.0.0.0', int(Port)))
	sock.listen(10)

	while True:
		conn, addr = sock.accept()
		print(addr[0],":",addr[1])

	sock.close()

def help():
	print("Usage => {0} -h -p <Port>".format(sys.argv[0]))

def main(argv):
	Port= 0

	try:
		opts, args = getopt.getopt(argv, "hp:",["Port="])
	except getopt.GetoptError:
		help()
		sys.exit(1)

	print(opts)

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

