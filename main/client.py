#coding:utf-8

import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 10000)
sock.connect(server_address)

# Send data
print("Envoie d'un message vers le serveur")
message = "Test de connexion avec le serveur"
sock.send(message.encode())

#data = sock.recv(16)
#print(data.decode());