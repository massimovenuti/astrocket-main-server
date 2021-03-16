#coding:utf-8

import socket
import requests

host, port = ('',10000) 

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind((host,port))

##### Listes de tuples (Name,port,adress)
server_list = [("Orion",1024,"localhost")]
#####

print("Server is up and running ...\n")

while True:
    socket.listen(10) # 10 connexions échouée avant de refuser
    print("Listening ...\n")
    conn, address = socket.accept()
    print("Accept connection ...\n")

    user_token = conn.recv(80)
    user_token.decode("utf8")


    # r = requests.post('https://auth.aw.alexandre-vogel.fr/user/check', data = {'user_token' : user_token})*

    # if r.status_code == 400 or r.status_code == 401
    #    print(r.json)
    #else
    #    print("Valid user")


    



conn.close()
socket.close()
    