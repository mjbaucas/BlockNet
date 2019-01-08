import socket
import json

from node_class import Device

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(('192.168.0.103', 9999))

device = Device("Dev00001", "02567435285")
    

while 1:
	userInput = raw_input("")
	message = json.dumps({"type": "access", "res_energy": 5, "rssi": -69, "mess": userInput})
	result, signature = device.dig_sign(message)
	message = device.encrypt(message + signature)
	if result:
		client.send(message);
		response = client.recv(4096)
		print response
