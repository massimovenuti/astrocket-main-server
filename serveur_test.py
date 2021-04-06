import asyncio
import time
import subprocess
import shlex
import os
import sys

class GameServer:
    def __init__(self, token, port):
        self.token=token
        self.port = port
        self.proc = None

    def start(self):
        args = shlex.split("./exec {} {}".format(self.port, self.token))
        self.proc = subprocess.Popen(args, stdout=sys.stdout, stderr=sys.stderr)

def find_server_pid(pid, server_list):
    for server in server_list:
        if server.proc.pid == pid:
            return server

def init_serveur():
    server_list = []
    token_list = []

    with open("server_list.txt", "r") as fp:
        for _, line in enumerate(fp):
            info = line.split(" ")
            token_list.append(info[0])
            server_list.append(GameServer(info[0], info[1]))

    return server_list, token_list

def manage_server(server_list):
    for server in server_list:
        server.start()
    
    while 1:
        pid, status = os.wait()
        proc = find_server_pid(pid, server_list)
        proc.start

