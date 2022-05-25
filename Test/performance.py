import argparse
import zmq
import timeit
from _thread import *
import logging
import os
import zmq

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.setsockopt_string(zmq.SUBSCRIBE, "")


def connect(addr: str, port, log: logging, type: str):
    socket.connect(f"tcp://{addr}:{port}")
    while True:
        start_time = timeit.default_timer()
        socket.recv()
        os.system("echo "+str(timeit.default_timer()-start_time) + " >> performance.txt")


if __name__ == "__main__":
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
    if isinstance(args.port, list):
        for i in range(0, len(list(args.port))):
            start_new_thread(connect, (args.addr, args.port[i], logging, args.sentype))
    else:
        start_new_thread(connect, (args.addr, args.port, logging, args.sentype))
        
    while 1:
        pass
