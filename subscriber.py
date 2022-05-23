import argparse
from _thread import *
import hashlib
import logging
from getpass import getpass
import os
import zmq
from Models.Monitor import Monitor
SYSTEM_PORT = 5554
from termcolor import colored

def user_validation(user: str) -> bool:
    with open("DB/allowed.txt") as f:
        lines = f.readlines()
        data = [
            (line.strip().split(",")[0], line.strip().split(",")[1]) for line in lines
        ]

        for d in data:
            if (
                d[0] == user
                and hashlib.md5(getpass("Password:").encode()).hexdigest().upper() == d[1]
            ):
                return True

    return False


def connect(addr: str, port, log: logging, type: str):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(f"tcp://{addr}:{port}")
    socket.setsockopt_string(zmq.SUBSCRIBE, "")
    pub = context.socket(zmq.PUB)
    pub.bind(f"tcp://{args.addr}:{SYSTEM_PORT}")
    while True:
        message = socket.recv()
        m = message.decode()
        if m.split(":")[0].strip() == type:
            if Monitor().checkQualityParameters(
                type=m.split(":")[0].strip(),
                value=float(m.split(":")[1].strip()),
            ):
                print(colored(m,'green'))
                log.info(m.split(":")[0] + ":" + m.split(":")[1])
            else:
                pub.send(type.encode()+ b': ' + m.split(":")[1].strip().encode())
        else:
            print(
                "Running monitor doesn't support " + m.split(":")[0].strip() + " sensor"
            )
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Publisher/suscriber implementation")
    parser.add_argument(
        "--port", "-p", nargs="*", default=5555, type=int, help="port number"
    )
    parser.add_argument(
        "--addr", "-a", default="127.0.0.1", type=str, help="Ip address IPV4"
    )
    parser.add_argument("--user", "-u", type=str, help="Username")
    parser.add_argument(
        "--type",
        "-t",
        required=True,
        default="Monitor",
        type=str,
        help="Type [SistemaC]",
        choices=["SistemaC", "Monitor"],
    )
    parser.add_argument(
        "--sentype",
        "-s",
        type=str,
        help="Sensor type",
        choices=["Ph", "Temperatura", "Oxigeno"],
    )
    args = parser.parse_args()
    context = zmq.Context()
    # User validation
    if args.type == "SistemaC" and args.user != None:
        # -------------------------------------
        if user_validation(args.user):
            socket = context.socket(zmq.SUB)
            socket.connect(f"tcp://{args.addr}:{SYSTEM_PORT}")
            socket.setsockopt_string(zmq.SUBSCRIBE, "")
            while True:
                message = socket.recv()
                print(colored(message.decode(),'red'))
        else:
            print("Incorrect information")

    elif (
        args.type == "Monitor"
        and not (vars(args)["sentype"] == None)
        and (
            "Ph" in vars(args)["sentype"]
            or "Temperatura" in vars(args)["sentype"]
            or "Oxigeno" in vars(args)["sentype"]
        )
    ):

        logging.basicConfig(
            filename="log.txt",
            level=logging.INFO,
            format="{asctime} {levelname:<8} {message}",
            style="{",
        )
        if isinstance(args.port, list):
            for i in range(0, len(list(args.port))):
                start_new_thread(
                    connect, (args.addr, args.port[i], logging, args.sentype)
                )
        else:
            start_new_thread(connect, (args.addr, args.port, logging, args.sentype))
        while 1:
            pass
    elif args.type == "SistemaC" and args.user == None:
        print("SistemaC required an user for authentication")
    else:
        print(
            'Param -s is required when u specified monitor as type\nPossibles entries for -s\nchoices=["Ph", "Temperatura", "Oxigeno"]'
        )
