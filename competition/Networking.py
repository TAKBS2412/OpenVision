import socket
from networktables import NetworkTables
import printer
'''
This class sends messages to the roboRIO via UDP.
'''
class Networking:
	# Constructor, initializes the UDP socket or NetworkTable depending on the protocol.
	def __init__(self, constants):
		self.ip = constants.getValue("ip")
		self.port = constants.getValue("port")
		if constants.getValue("protocol") == "NT":
			NetworkTables.initialize(server=self.ip)
			self.sd = NetworkTables.getTable(constants.getValue("tablename"))
		elif constants.getValue("protocol") == "UDP":
			self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		else:
			printer.printIfNeeded("Invalid protocol specified! Valid protocols are NT and UDP.", constants)

	# Sends data to the roboRIO, using UDP or NetworkTables, depending on the value of protocol in constants.
	def sendData(self, constants, angle, distance, doextake, targetsFound):
		if constants.getValue("protocol") == "NT":
			self.sendDataNT(self.sd, angle, distance, doextake, targetsFound)
		elif constants.getValue("protocol") == "UDP":
			self.sendDataUDP(angle, distance, doextake, targetsFound)
		else:
			printer.printIfNeeded("Invalid protocol specified! Valid protocols are NT and UDP.", constants)

	# Sends data to the roboRIO via UDP (this is currently blocking)
	def sendDataUDP(self, angle, distance, doextake, targetsFound):
		self.message = str(angle) + ";" + str(distance) + ";" + str(doextake) + ";" + str(targetsFound)
		self.socket.sendto(self.message, (self.ip, self.port))

	# Sends data using NetworkTables.
	def sendDataNT(self, sd, angle, distance, doextake, targetsFound):
		# Send the variables to the roboRIO
		sd.putNumber("angle", angle)
		sd.putNumber("distance", distance)
		sd.putBoolean("doextake", doextake) 
		sd.putBoolean("targetsFound", targetsFound)

