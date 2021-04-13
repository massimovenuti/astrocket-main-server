import asyncio
import time
import subprocess
import shlex
import os
import sys
import requests
import socket

from dotenv import load_dotenv

load_dotenv()

class GameServer:
    def __init__(self, port, name):
        self.token = None
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

def init_server(token):
    server_list = []
    token_list = []
    with open("server_list.txt", "r") as fp:
        for _, line in enumerate(fp):
            info = line.split(" ")
            server_list.append(GameServer(info[0], info[1]))

    for server in server_list:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)

        parameters = {'name':server.name, 'address':local_ip, 'port':int(server.port)}
        header = {"user_token":token["token"]}

        r = requests.post('http://localhost:3500/main/GameServer', json=parameters, headers=header)

        #r = requests.post('http://main.aw.alexandre-vogel.fr:3500/main/GameServer', json=parameters, headers=token)
        if (r.status_code == 200):
            server.start()
            token_list.append(r.text)
            server.token = r.text
            print("Server " + server.name + " has started") 
        elif (r.status_code == 404 or r.status_code == 405 or r.status_code == 406):
            print("Server " + server.name + " hasn't started because some parameters are missing or are invalid")
        elif (r.status_code == 402 or r.status_code == 403):
            print("Server " + server.name + " hasn't started because some parameters are already used")
        elif (r.status_code == 401):
            print("Server " + server.name + " hasn't started because user main can't create servers")
        else:
            print("Server " + server.name + " hasn't started because bigMain doesn't respond")

    return server_list, token_list

def manage_server(server_list):

    while 1:
        pid, status = os.wait()
        proc = find_server_pid(pid, server_list)
        proc.start

def print_server(server_list):
    for server in server_list:
        print("Serveur " + server.name + " listening on port " + server.port)

def alive_checker(token_list,token,server_list):
    subprocess.call(['python3','life_check.py',token,str(len(token_list))]+token_list+server_list)


print("Server running ...")

PARAMS = {'username':os.environ.get("NAME"),'password':os.environ.get("PASSWORD")}
#r = requests.post('http://main.aw.alexandre-vogel.fr:3010/user/login', json=PARAMS)
r = requests.post('http://localhost:8080/user/login', json=PARAMS)
if (r.status_code == 400 or r.status_code == 402 or r.status_code == 403):
    print("Some parameters are missing or invalid")
elif (r.status_code == 401):
    print("User main has been banned")
elif (r.status_code == 500):
    print("Authentification API doesn't respond")
else:
    server_list, token_list = init_server(r.json())
    alive_checker(token_list,r.json()["token"],server_list)
    print_server(server_list)
    manage_server(server_list)