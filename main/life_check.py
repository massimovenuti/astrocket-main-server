import psutil, os, time, requests, sys
me = psutil.Process(os.getpid())

while me.parent is not None:
    print("Operating main server")

    parameters = {'array' : sys.argv[0]}
    r = requests.post('http://main.aw.alexandre-vogel.fr:3500/main/alive', data=parameters)

    if (r.status_code == 200):
        print("Successfull alive checking")
    elif (r.status_code == 400):
        print("Parameters are missing or invalid")
    elif (r.status_code == 401 or r.status == 402):
        print("Server doesn't exist")
    else:
        print("BigMain doesn't respond")
    

    
print("Main server disappear")

for server in sys.argv[2]:
    parameters = {'name' : server.name}
    r = requests.delete('http://main.alexandre-vogel.fr/main/GameServer', data=parameters, headers=sys.argv[1])

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
