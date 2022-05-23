import argparse
import os
import subprocess
from _thread import *
from termcolor import colored
from time import sleep

parser = argparse.ArgumentParser(description="Publisher/suscriber implementation")
parser.add_argument(
    "--addr", "-a", nargs="+", required=True, help="port number"
)
args = parser.parse_args()

def ping(ip):
    ping_reply = subprocess.run(
        ["ping", "-c", "2", ip], stderr=subprocess.PIPE, stdout=subprocess.PIPE
    )
    if ping_reply.returncode == 0:
        # ping will return 0 success if destination is unreachable so I have to check this
        if "unreachable" in str(ping_reply.stdout):
            print(colored("RIP %s" % ip, "red"))
        else:
            print(colored("BEATING %s" % ip, "green"))
    elif ping_reply.returncode == 1:
         print(colored("RIP %s" % ip,"red"))
   

while True:
    for ip in args.addr:
        start_new_thread(ping, (ip,))
    sleep(5)
