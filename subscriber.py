import argparse
from _thread import *
import hashlib
import logging
import zmq

from Monitor import Monitor


def user_validation(user: str) -> bool:
    with open("DB/allowed.txt") as f:
        lines = f.readlines()
        data = [
            (line.strip().split(",")[0], line.strip().split(",")[1]) for line in lines
        ]

        for d in data:
            if (
                d[0] == user
                and hashlib.md5(input("Password:").encode()).hexdigest().upper() == d[1]
            ):
                return True
    return False


def connect(addr: str, port, log: logging):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(f"tcp://{addr}:{port}")
    socket.setsockopt_string(zmq.SUBSCRIBE, "")
    while True:
        message = socket.recv()
        m=message.decode()
        if Monitor().checkQualityParameters(
            type=m.split(":")[0].strip(),
            value=float(m.split(":")[1].strip()),
        ):
            print(m)
            log.info(
                m.split(":")[0] + ":" + m.split(":")[1]
            )


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
        default="SistemaC",
        type=str,
        help="Type [SistemaC]",
        choices=["SistemaC", "Monitor"],
    )
    args = parser.parse_args()

    context = zmq.Context()
    # User validation
    if args.type == "SistemaC" and user_validation(args.user):
        # -------------------------------------
        socket = context.socket(zmq.SUB)
        socket.connect(f"tcp://{args.addr}:{args.port[0]}")
        socket.setsockopt_string(zmq.SUBSCRIBE, "")
        while True:
            message = socket.recv()
            print(message.decode())

    elif args.type == "Monitor":
        logging.basicConfig(
            filename="log.txt",
            level=logging.INFO,
            format="{asctime} {levelname:<8} {message}",
            style="{",
        )
        for i in range(0, len(args.port)):
            start_new_thread(connect, (args.addr, args.port[i], logging))
        while 1:
            pass
