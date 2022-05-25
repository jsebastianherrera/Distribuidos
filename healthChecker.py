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
        'ps aux | grep "python3 monitor.py" | awk \'{printf $2 " " }{for(i=11;i<=NF;i++) printf  $i " "}{print " " }\' > output.txt'
    )
    with open("output.txt") as f:
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
                    data[p] = ("R", value[1], value[2], value[3])
                    print(
                        now.strftime("%H:%M:%S")
                        + colored(" " + p + " " + str(value) + " BEATING", "green")
                    )
                else:
                    data[p] = ("T", value[1], value[2], value[3])
                    print(
                        now.strftime("%H:%M:%S")
                        + colored(" " + p + " " + str(data[p]) + " DIED", "red")
                    )

        elif len(data) > 0:
            print("start monitor again")

        else:
            print("No monitors are running")


def getPairs() -> dict:

    os.system(
        'ps aux | grep "python3 monitor.py" | awk \'{printf $2 " " }{for(i=11;i<=NF;i++) printf  $i " "}{print " " }\'  > output.txt'
    )
    with open("output.txt") as f:
        lines = f.readlines()
        lines.pop()
        lines.pop()
        keys = list()
        values = list()
        if len(lines) > 0:
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
                values.append((state, sen, addr, port))
            return dict(zip(keys, values))
        else:
            print("No monitor running in this machine")
            return None


if __name__ == "__main__":
    data = getPairs()
    while True:
        check()
        sleep(5)
