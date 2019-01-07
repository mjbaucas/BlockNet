import socket
import threading

from node_class import Node, Device

node_private_key = "NoDe0001"
server_node = Node("NoDe0001")

bind_ip = '192.168.0.103'
bind_port = 9999

mess = server_node.encrypt("NoDe0001", "Hello World")
print mess
print server_node.decrypt(mess)

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
        args=(client_sock,)  # without comma you'd get a... TypeError: handle_client_connection() argument after * must be a sequence, not _socketobject
    )
    client_handler.start()
