import socket
import json

from node_class import Device, Node

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(('192.168.0.103', 9999))

device_one = Device("Device0001", "device1-private.pem")
device_one.pair_device("NoDe0001", "server-public.pem")    

while 1:
	userInput = raw_input("")
	
	data = json.dumps({"type": "access", "id": "Device0001"})
	message = device_one.process_network_message(data)
	if message is not None:
		client.send(message);
		response = client.recv(4096)
		print response
