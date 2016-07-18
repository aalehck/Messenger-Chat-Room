#!/usr/bin/env python
import zmq

def main():

	context = zmq.Context()
	respSock = context.socket(zmq.REP)
	pubSock = context.socket(zmq.PUB)
	respSock.bind("tcp://*:5555")
	pubSock.bind("tcp://*:5563")

	while True:

		[ protocol, message] = respSock.recv_multipart()

		respSock.send(message)
		pubSock.send_multipart([b"{protocol}".format(protocol=protocol), b"{message}".format(message=message)])

if __name__ == "__main__":
	main()
