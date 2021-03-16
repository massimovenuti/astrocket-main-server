#coding:utf-8

import socket
import requests

host, port = ('',10000) 

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind((host,port))
print("Server is up and running ...\n")

while True:
    socket.listen(10) # 10 connexions échouée avant de refuser
    print("Listening ...\n")
    conn, address = socket.accept()
    print("Accept connection ...\n")

    user_token = conn.recv(80)
    user_token.decode("utf8")


    # x = requests.post('https://auth.aw.alexandre-vogel.fr/', data = {'user_token' : user_token})



conn.close()
socket.close()
    