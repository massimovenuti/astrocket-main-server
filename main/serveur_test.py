import time
import subprocess
import shlex
import os
import sys
import requests
import socket
import json

class GameServer:
    def __init__(self, exec_file, port, name):
        self.token = None
        self.exec_file = exec_file
        self.port = port
        self.name = name
        self.proc = None

    def start(self):
        args = shlex.split("{} {} {}".format(self.exec_file, self.port, self.token))
        self.proc = subprocess.Popen(args, stdout=sys.stdout, stderr=sys.stderr)

    def intoTab(self):
        #tab = [self.token,self.port,self.name]
        tab = self.name
        return tab

def find_server_pid(pid, server_list):
    for server in server_list:
        if server.proc.pid == pid:
            return server

def init_server(token, exec_file):
    server_list = []
    token_list = []
    with open("server_list.txt", "r") as fp:
        for _, line in enumerate(fp):
            info = line.split(" ")
            server_list.append(GameServer(exec_file, info[0], info[1]))

    for server in server_list:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)

        parameters = {'name':server.name, 'address':local_ip, 'port':int(server.port)}
        header = {"user_token":token["token"]}

        r = requests.post('https://main.aw.alexandre-vogel.fr:3500/main/GameServer', json=parameters, headers=header)
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
        pid, _ = os.wait()
        proc = find_server_pid(pid, server_list)
        proc.start

def print_server(server_list):
    for server in server_list:
        print("Serveur " + server.name + " listening on port " + server.port)

def alive_checker(token_list,token,server_list):
    
    server_list_tab = []
    for server in server_list:        
        server_list_tab.append(server.intoTab())

    subprocess.call(['python3','life_check.py',token,str(len(token_list))]+token_list+server_list_tab)

if __name__ == "__main__":
    with open("{}/conf.json".format(os.path.dirname(__file__))) as conf_file:
        conf = json.load(conf_file)

    print("Server running ...")

    PARAMS = {'username':conf["username"],'password':conf["password"]}
    r = requests.post('https://auth.aw.alexandre-vogel.fr:3010/user/login', json=PARAMS)
    if (r.status_code == 400 or r.status_code == 402 or r.status_code == 403):
        print("Some parameters are missing or invalid")
    elif (r.status_code == 401):
        print("User main has been banned")
    elif (r.status_code == 500):
        print("Authentification API doesn't respond")
    else:
        server_list, token_list = init_server(r.json(), conf["exec"])
        alive_checker(token_list,r.json()["token"],server_list)
        print_server(server_list)
        manage_server(server_list)
