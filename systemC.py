import argparse
from getpass import getpass
import hashlib
import logging
import zmq
from termcolor import colored
from _thread import *


SYSTEM_PORT = 5554


def connect(pull: zmq.Socket):
    while True:
        m = pull.recv().decode()
        logging.info(m.split(":")[0] + ":" + m.split(":")[1])
        print(colored(m, "red"))


def user_validation(user: str) -> bool:
    with open("DB/allowed.txt") as f:
        lines = f.readlines()
        data = [
            (line.strip().split(",")[0], line.strip().split(",")[1]) for line in lines
        ]
        for d in data:
            if (
                d[0] == user
                and hashlib.md5(getpass("Password:").encode()).hexdigest().upper()
                == d[1]
            ):
                return True
    return False


if __name__ == "__main__":
    logging.basicConfig(
        filename=f"DB/sistemaC.txt",
        level=logging.INFO,
        format="{asctime} {levelname:<8} {message}",
        style="{",
    )

    parser = argparse.ArgumentParser(description="SystemC implementation")
    parser.add_argument("--user", "-u", required=True, type=str, help="Username")
    args = parser.parse_args()
    if user_validation(args.user):
        context = zmq.Context()
        zmq_socket = context.socket(zmq.PULL)
        zmq_socket.bind(f"tcp://*:{SYSTEM_PORT}")
        start_new_thread(connect, (zmq_socket,))
        while True:
            pass

    else:
        print("Incorrect information")
