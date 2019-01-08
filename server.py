import socket
import threading

from node_class import Node, Device

node_private_key = "NoDe0001"
server_node = Node("NoDe0001", "server-private.pem")
device_one = Device("Device0001", "device1-private.pem")

bind_ip = '192.168.0.103'
bind_port = 9999

mess = server_node.encrypt("Device0001", "Hello World")
#print mess
#if mess is not None:
#    print device_one.decrypt(mess)
    
sign = device_one.sign("Message")
print device_one.verify("Message1212", sign)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)  # max backlog of connections

print 'Listening on {}:{}'.format(bind_ip, bind_port)


def handle_client_connection(client_socket):
    while True:
	request = client_socket.recv(1024)
	if server_node.process_message(request):
	    client_socket.send('Access Granted')
	else:
	    client_socket.send('Access Blocked')

while True:
    client_sock, address = server.accept()
    print 'Accepted connection from {}:{}'.format(address[0], address[1])
    client_handler = threading.Thread(
        target=handle_client_connection,
        args=(client_sock,)  
    )
    client_handler.start()
