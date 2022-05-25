import argparse
from _thread import *
from _thread import *
import hashlib
import logging
from getpass import getpass
import os
import signal
import subprocess
from time import sleep
import zmq
from Models.Monitor import Monitor
from termcolor import colored

SYSTEM_PORT = 5554
SYSTEM_IP = "192.168.0.56"
context = zmq.Context()
push = context.socket(zmq.PUSH)
socket = context.socket(zmq.SUB)
socket.setsockopt_string(zmq.SUBSCRIBE, "")


def start(signum, frame):
    print(colored("Starting replica.."))
    if isinstance(args.port, list):
        for i in range(0, len(list(args.port))):
            start_new_thread(connect, (args.addr, args.port[i], logging, args.sentype))
    else:
        start_new_thread(connect, (args.addr, args.port, logging, args.sentype))
    while 1:
        pass

def reload(signum, frame):
    print("Zzz")
    socket.close()
    push.close()
            
        


def connect(addr: str, port, log: logging, type: str):
    socket.connect(f"tcp://{addr}:{port.strip()}")

    while True:
        message = socket.recv()
        m = message.decode()
        if m.split(":")[0].strip() == type:
            if Monitor().checkQualityParameters(
                type=m.split(":")[0].strip(),
                value=float(m.split(":")[1].strip()),
            ):
                print(colored(m, "green"))
                log.info("Replica " + m.split(":")[0] + ":" + m.split(":")[1])
            else:
                push.connect(f"tcp://{SYSTEM_IP}:{SYSTEM_PORT}")
                push.send(m.encode())
                print(colored(m, "red"))

        else:
            print(
                "Running monitor doesn't support " + m.split(":")[0].strip() + " sensor"
            )
            break


if __name__ == "__main__":

    signal.signal(signal.SIGUSR1, reload)
    signal.signal(signal.SIGINT, start)
    parser = argparse.ArgumentParser(description="Publisher/suscriber implementation")
    parser.add_argument("--port", "-p", nargs="*", required=True, help="port number")
    parser.add_argument("--addr", "-a", required=True, type=str, help="Ip address IPV4")

    parser.add_argument(
        "--sentype",
        "-s",
        type=str,
        required=True,
        help="Sensor type",
        choices=["Ph", "Temperatura", "Oxigeno"],
    )
    args = parser.parse_args()
    logging.basicConfig(
        filename="log.txt",
        level=logging.INFO,
        format="{asctime} {levelname:<8} {message}",
        style="{",
    )
    while True:
        pass
