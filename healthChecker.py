import argparse
import os
import subprocess
from _thread import *
from termcolor import colored
from time import sleep

parser = argparse.ArgumentParser(description="Healthcheck")
parser.add_argument(
    "--num", "-n",  required=True, help="Quantity"
)
args = parser.parse_args()

def check():
    output=subprocess.run(["ps","aux","|","grep","\"python3 monitor.py\"","|","awk","'{printf $2 " " }{for(i=11;i<=NF;i++) printf  $i " "}{print " " }'","2>&1"],capture_output=True).stdout
    print(output.strip().decode())
monitors=list()
while True:
    start_new_thread(check,())
    sleep(5)
