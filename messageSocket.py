import zmq

def getIpAddress(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915, # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

class messageClient:
	#AccountName: user name
	#Host: host server address
	#Context: socket context for this application
	#Request: request socket for sending messages to host server
	#Subscribers: list of subscriber sockets for receiving messages from other clients

	def __init__(self, host, accountName):

		#Create message forwarding connection
		self.host = host
		self.accountName = accountName
		self.context = zmq.Context()
		self.request = self.context.socket(zmq.REQ)
		self.request.connect("tcp://{ip}:5555".format(ip=host))

		#Create PUB/SUB connection
		self.subscriber = self.context.socket(zmq.SUB)
		self.subscriber.connect("tcp://{ip}:5563".format(ip=self.host))

	# Send request for connection for a conversation
	def createNewConnection(self, connectionName):

		self.subscriber.setsockopt(zmq.SUBSCRIBE, b"{connectionName}".format(connectionName=connectionName))

	def sendMessage(self, host, message):
		self.request.send_multipart([b"{host}".format(host=host), b"{name}: {message}".format(name=self.accountName, message=message)])
		reply = self.request.recv()
		print reply
