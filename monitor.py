import argparse
from _thread import *
from _thread import *
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


def resume(signum, frame):
    with open("Trash/pids.txt") as f:
        lines = f.readlines()
        for line in lines:
            split = line.split(" ")
            if split[0].strip() == str(os.getpid()):
                subprocess.run(["kill", "-USR1", str(split[1]).strip()])
        print(colored("Monitor is back..."))
        if isinstance(args.port, list):
            for i in range(0, len(list(args.port))):
                start_new_thread(
                    connect, (args.addr, args.port[i], logging, args.sentype)
                )
        else:
            start_new_thread(connect, (args.addr, args.port, logging, args.sentype))
        while 1:
            pass


def handler(signum, frame):
    print(colored("Interrupting monitor ..."))
    for i in args.port:
        socket.disconnect(f"tcp://{args.addr}:{i}")
    try:
        push.disconnect(f"tcp://{SYSTEM_IP}:{SYSTEM_PORT}")
    except:
        print("")
    subprocess.run(["kill", "-STOP", str(os.getpid())])


def connect(addr: str, port, log: logging, type: str):
    socket.connect(f"tcp://{addr}:{port}")

    while True:
        message = socket.recv()
        m = message.decode()
        if m.split(":")[0].strip() == type:
            if Monitor().checkQualityParameters(
                type=m.split(":")[0].strip(),
                value=float(m.split(":")[1].strip()),
            ):
                print(colored(m, "green"))
                log.info(m.split(":")[0] + ":" + m.split(":")[1])
            else:
                log.info("Redi -> SistemaC: " + m.split(":")[0] + ":" + m.split(":")[1])
                push.connect(f"tcp://{SYSTEM_IP}:{SYSTEM_PORT}")
                push.send(m.encode())
                print(colored(m, "red"))

        else:
            print(
                "Running monitor doesn't support " + m.split(":")[0].strip() + " sensor"
            )
            break


if __name__ == "__main__":
    signal.signal(signal.SIGCONT, resume)
    signal.signal(signal.SIGINT, handler)
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
        filename=f"DB/mon{args.sentype}.txt",
        level=logging.INFO,
        format="{asctime} {levelname:<8} {message}",
        style="{",
    )
    pp = ""
    if isinstance(args.port, list):
        for i in list(args.port):
            pp += str(i) + " "
        subprocess.Popen(
            ["python3", "replica.py", "-a", args.addr, "-s", args.sentype, "-p", pp],
        )

        for i in range(0, len(list(args.port))):
            start_new_thread(connect, (args.addr, args.port[i], logging, args.sentype))
    else:
        subprocess.Popen(
            [
                "python3",
                "replica.py",
                "-a",
                args.addr,
                "-s",
                args.sentype,
                "-p",
                args.port,
            ]
        )
        start_new_thread(connect, (args.addr, args.port, logging, args.sentype))
    while 1:
        pass
