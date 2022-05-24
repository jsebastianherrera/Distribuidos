import argparse
from getpass import getpass
import hashlib
import zmq
from termcolor import colored
from _thread import *

from Models.Monitor import Monitor

SYSTEM_PORT = 5554
SYSTEM_IP = "192.168.0.56"


def connect(pull: zmq.Socket):
    while True:
        message = pull.recv()
        m = message.decode()
        if m.split(":")[0].strip() == type:
            if Monitor().checkQualityParameters(
                type=m.split(":")[0].strip(),
                value=float(m.split(":")[1].strip()),
            ):
                print(colored(m, "green"))

            else:
                print(colored(m, "red"))

        else:
            print(
                "Running monitor doesn't support " + m.split(":")[0].strip() + " sensor"
            )
            break


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
