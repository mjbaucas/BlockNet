import socket
import threading

from node_class import Node, Device

server_node = Node("NoDe0001", "server-private.pem")

bind_ip = '192.168.0.103'
bind_port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)  # max backlog of connections

print 'Listening on {}:{}'.format(bind_ip, bind_port)


def handle_client_connection(client_socket):
    while True:
	request = client_socket.recv(4096)
	message = server_node.read_message(request)
	print(message)
	if message is not None:
	    response = server_node.process_message(message)
	    if response is not None:
		client_socket.send(response)

while True:
    client_sock, address = server.accept()
    print 'Accepted connection from {}:{}'.format(address[0], address[1])
    client_handler = threading.Thread(
        target=handle_client_connection,
        args=(client_sock,)  
    )
    client_handler.start()
