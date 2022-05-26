import argparse
from _thread import *
import logging
import signal
import zmq
import re
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
    data = re.findall("55[0-9]+", str(args.port))
    for i in data:
            start_new_thread(
                connect, (args.addr, i, logging, args.sentype)
            )
    while 1:
        pass


def reload(signum, frame):
    print("Zzz")
    socket.close()
    push.close()


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
                log.info("Replica " + m.split(":")[0] + ":" + m.split(":")[1])
            else:
                push.connect(f"tcp://{SYSTEM_IP}:{SYSTEM_PORT}")
                push.send(m.encode())
                log.info(
                    "Replica red-> SistemaC " + m.split(":")[0] + ":" + m.split(":")[1]
                )
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
        filename=f"DB/mon{args.sentype}.txt",
        level=logging.INFO,
        format="{asctime} {levelname:<8} {message}",
        style="{",
    )
    while True:
        pass
