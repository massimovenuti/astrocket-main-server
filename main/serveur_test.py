import asyncio
import time
import subprocess
import shlex
import os
import sys
import requests
import socket

#from dotenv import load_dotenv

#load_dotenv()

class GameServer:
    def __init__(self, token, port, name):
        self.token = token
        self.port = port
        self.name = name
        self.proc = None

    def start(self):
        # args = shlex.split("./exec {} {}".format(self.port, self.token))
        self.proc = subprocess.Popen("./mock_file", stdout=sys.stdout, stderr=sys.stderr)

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

def manage_server(server_list,token):
    for server in server_list:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)

        parameters = {'name':server.name, 'address':local_ip, 'port':server.port}
        headers = {'user_token': os.environ.get("TOKEN")}
        r = requests.post('http://localhost:3500/main/GameServer', data=parameters, headers=headers)

        if (r.status_code == 200):
            server.start()
            print("Server " + server.name + " has started") 
        elif (r.status_code == 404 or r.status_code == 405 or r.status_code == 406):
            print("Server " + server.name + " hasn't started because some parameters are missing or are invalid")
        elif (r.status_code == 402 or r.status_code == 403):
            print("Server " + server.name + " hasn't started because some parameters are already used")
        elif (r.status_code == 401):
            print("Server " + server.name + " hasn't started because user main can't create servers")
        else:
            print("Server " + server.name + " hasn't started because bigMain doesn't respond")

    while 1:
        pid, status = os.wait()
        proc = find_server_pid(pid, server_list)
        proc.start

def print_server(server_list):
    for server in server_list:
        print("Serveur " + server.name + " listening on port " + server.port,)


print("Server running ...")

parameters = {"username": "Main", "password":"main"}
r = requests.post('http://localhost:3010/user/login', data=parameters)

if (r.status_code == 400 or r.status_code == 402 or r.status_code == 403):
    print("Some arguments are missing or invalid")
elif (r.status_code == 401):
    print("User main has been banned")
else:
    print("Authentification API doesn't respond")

server_list, token_list = init_server()
print_server(server_list)
manage_server(server_list,r.json)

