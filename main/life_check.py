import psutil, os, time, requests, sys

token = sys.argv[1]
size = sys.argv[2]
token_list = sys.argv[3:3+int(size)]
server_list = sys.argv[3+int(size):]
me = psutil.Process(os.getpid())

while me.parent is not None:
    print("Operating main server")

    parameters = []
    for token in token_list:
        parameters.append({"serverToken": token})
    #r = requests.post('http://main.aw.alexandre-vogel.fr:3500/main/alive', json=parameters)
    r = requests.post('http://localhost:3500/main/alive', json=parameters)

    if (r.status_code == 200):
        print("Successfull alive checking")
        time.sleep(5)
    elif (r.status_code == 400):
        print("Parameters are missing or invalid")
    elif (r.status_code == 401 or r.status == 402):
        print("Server doesn't exist")
    else:
        print("BigMain doesn't respond")
        
print("Main server disappear")

for i in range (len(server_list)):
    parameters = {'name' : server_list[i]}
    #r = requests.delete('http://main.alexandre-vogel.fr:3500/main/GameServer', json=parameters, headers=sys.argv[1])
    r = requests.delete('http://localhost:3500/main/GameServer', json=parameters, headers=token)

    if (r.status_code == 200):
        print("Successfull deleting")
    elif (r.status_code == 400 or r.status_code == 401):
        print("Parameters are missing or invalid")
    elif (r.status_code == 402):
        print("Server doesn't exist")
    elif (r.status == 403):
        print("User main can't delete servers")
    else:
        print("BigMain doesn't respond")

