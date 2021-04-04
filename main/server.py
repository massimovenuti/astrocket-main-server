#coding:utf-8
import subprocess
import sys
import time
import http

# Liste de serveurs
# Un serveur => tuple (Nom,Port,Nbr_joueurs)
server_list = [(),()]
result = []
#####

print("Main is up and running ...\n")

while True:

    for i in range(len(server_list)):
        # Ajout d'éléments dans la liste pour les arguments
        # Ligne de test pour vérifier qu'un processus est vivant ou mort
        result.append(subprocess.Popen([sys.executable,"-c", "import time\ntime.sleep("+ str(i*10) +")"]))

    print("Checking process status ...")

    # Vérification de l'état d'un processus
    for i in range(len(server_list)):
        if result[i].poll() is None:
            print("("+str(i)+") Processus alive")
        else:
            print("("+str(i)+") Processus dead")

    time.sleep(5)


    