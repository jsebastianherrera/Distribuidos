import argparse
from base64 import encode
import hashlib
from unittest import result
import zmq


def user_validation(user: str) -> bool:
    with open("DB/allowed.txt") as f:
        lines = f.readlines()
        data = [
            (line.strip().split(",")[0], line.strip().split(",")[1]) for line in lines
        ]

        for d in data:
            if d[0] == user and hashlib.md5(input("Password:").encode()).hexdigest().upper() == d[1]:
                return True
    return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Publisher/suscriber implementation")
    parser.add_argument("--port", "-p", default=5555, type=int, help="port number")
    parser.add_argument(
        "--addr", "-a", default="127.0.0.1", type=str, help="Ip address IPV4"
    )
    parser.add_argument("--user", "-u", type=str, help="Username",required=True)
    parser.add_argument(
        "--type",
        "-t",
        default="SistemaC",
        type=str,
        help="Type [SistemaC]",
        choices=["SistemaC"],
    )
    args = parser.parse_args()
    # User validation
    if user_validation(args.user):
        # -------------------------------------
        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        socket.connect(f"tcp://{args.addr}:{args.port}")
        socket.setsockopt_string(zmq.SUBSCRIBE, "")
        while True:
            message = socket.recv()
            print(message.decode())
