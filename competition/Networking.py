import socket
'''
This class sends messages to the roboRIO via UDP.
'''
class Networking:
	# Constructor, initializes the UDP socket
	def __init__(self, ip, port):
		self.ip = ip
		self.port = port
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	# Sends data to the roboRIO via UDP (this is currently blocking)
	def sendData(self, angle, distance, doextake, targetsFound):
		self.message = str(angle) + ";" + str(distance) + ";" + str(doextake) + ";" + str(targetsFound)
		self.socket.sendto(self.message, (self.ip, self.port))
