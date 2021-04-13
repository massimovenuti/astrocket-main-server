import psutil, os, time, requests, sys
me = psutil.Process(os.getpid())

while me.parent is not None:
    print("Operating main server")

    parameters = {'array' : sys.argv[0]}
    r = requests.post('http://main.aw.alexandre-vogel.fr:3500/main/alive', data=parameters)

    if (r.status_code != 200)
        print("Alive doesn't work")

    
print("Main server disappear")

for server in sys.argv[2]:
    parameters = {'name' : server.name}
    r = requests.delete('http://main.alexandre-vogel.fr/main/GameServer', data=parameters, headers=sys.argv[1])

    if (r.status_code != 200)
        print("Cannot delete GS")
