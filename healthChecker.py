import subprocess
import os
import re
from _thread import *
from termcolor import colored
from time import sleep
from datetime import datetime


def check() -> bool:
    now = datetime.now()
    os.system(
        'ps aux | grep "python3 monitor.py" | awk \'{printf $2 " " }{for(i=11;i<=NF;i++) printf  $i " "}{print " " }\' > Trash/monitores.txt'
    )

    with open("Trash/monitores.txt") as f:
        lines = f.readlines()
        lines.pop()
        lines.pop()
        pid = list()
        if len(lines) > 0:
            for line in lines:
                pid.append(line.strip().split(" ")[0])
            for p in pid:
                state = (
                    subprocess.run(["ps", "-o", "state=", "-p", p], capture_output=True)
                    .stdout.decode()
                    .strip()
                )
                value = data[p]
                if state == "R":
                    data[p] = (value[0],"R", value[2], value[3], value[4])
                    print(
                        now.strftime("%H:%M:%S")
                        + colored(" " + p + " " + str(value) + " BEATING", "green")
                    )
                else:
                    data[p] = (value[0],"T", value[2], value[3], value[4])
                    print(
                        now.strftime("%H:%M:%S")
                        + colored(" " + p + " " + str(data[p]) + " DIED", "red")
                    )
                    #subprocess.run(["kill", "-USR1",str(data[p][0])])

        else:
            print("No monitors are running")


def getPairs() -> dict:

    os.system(
        'ps aux | grep "python3 monitor.py" | awk \'{printf $2 " " }{for(i=11;i<=NF;i++) printf  $i " "}{print " " }\'  > Trash/monitores.txt'
    )
    os.system(
        "ps aux | grep \"python3 replica.py\" | awk '{print $2}' > Trash/replicas.txt"
    )
    pids = list()
    with open("Trash/replicas.txt") as f:
        lines = f.readlines()
        lines.pop()
        lines.pop()
        for line in lines:
            pids.append(line.strip())
    with open("Trash/monitores.txt") as f:
        lines = f.readlines()
        lines.pop()
        lines.pop()
        keys = list()
        values = list()
        if len(lines) > 0:
            cont=0
            for line in lines:
                pid = line.strip().split(" ")[0]
                keys.append(pid)
                addr = re.search(
                    "([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)", line.strip()
                ).group()
                state = (
                    subprocess.run(
                        ["ps", "-o", "state=", "-p", pid], capture_output=True
                    )
                    .stdout.strip()
                    .decode()
                )
                port = ""
                sen = re.search("[A-Z][a-z]+", line.strip()).group()
                for r in re.findall("(55[0-9][0-9] )", line.strip()):
                    if r != pid:
                        port += r + " "
                os.system("echo \""+ pid+" "+pids[cont] +"\" >> Trash/pids.txt")
                values.append((pids[cont],state, sen, addr, port))
                cont+=1
            return dict(zip(keys, values))
        else:
            print("No monitor running in this machine")
            return None


if __name__ == "__main__":
    data = getPairs()
    while True:
        check()
        sleep(5)
