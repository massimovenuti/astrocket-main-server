import asyncio
import time
import subprocess
import shlex
import os
import sys
import requests
import socket

class GameServer:
    def __init__(self, token, port, name):
        self.token = token
        self.port = port
        self.name = name
        self.proc = None

    def start(self):
        args = shlex.split("./exec {} {}".format(self.port, self.token))
        self.proc = subprocess.Popen(args, stdout=sys.stdout, stderr=sys.stderr)

        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)

        parameters = {'name':self.name, 'address':local_ip, 'port':self.port}
        r = requests.post('https://main.aw.alexandre-vogel.fr/main/GameServer')

def find_server_pid(pid, server_list):
    for server in server_list:
        if server.proc.pid == pid:
            return server

def init_server():
    server_list = []
    token_list = []

    with open("server_list.txt", "r") as fp:
        for _, line in enumerate(fp):
            info = line.split(" ")
            token_list.append(info[0])
            server_list.append(GameServer(info[0], info[1], info[2]))

    return server_list, token_list

def manage_server(server_list):
    for server in server_list:
        server.start()
    
    while 1:
        pid, status = os.wait()
        proc = find_server_pid(pid, server_list)
        proc.start

def print_server(server_list):
    for server in server_list:
        print("Serveur " + server.name + " listening on port " + server.port,)


print("Server running ...")

server_list, token_list = init_server()
print_server(server_list)
# manage_server(server_list)

