from http.client import ImproperConnectionState
import os
import pathlib
from time import sleep
from Models.Ph import Ph
from Models.Oxigeno import Oxigeno
from Models.Temperatura import Temperatura
import argparse
import zmq
import signal


def handler(signum, frame):
    res = input("Ctrl-c was pressed. Do you really want to exit? y/n ")
    if res == "y":
        socket.close()
        path = os.path.abspath(__file__)
       # os.system("py " + path+" -s "+ args.sentype  )
        exit(1)


def sendInfo(generate):
    socket.bind(f"tcp://{args.addr}:{args.port}")
    while True:
        sleep(args.time)
        valor = str(generate.generateValues())
        socket.send(args.sentype.encode() + b": " + valor.encode())
        print(args.sentype + ":" + valor)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, handler)
    parser = argparse.ArgumentParser(description="Publisher/suscriber implementation")
    parser.add_argument("--port", "-p", default=5555, type=int, help="port number")
    parser.add_argument(
        "--addr", "-a", default="127.0.0.1", type=str, help="Ip address IPV4"
    )
    parser.add_argument(
        "--sentype",
        "-s",
        required=True,
        default="Ph",
        type=str,
        help="Sensor type",
        choices=["Ph", "Temperatura", "Oxigeno"],
    )
    parser.add_argument("--time", "-tm", default=10, type=int, help="Time")
    parser.add_argument(
        "--file", "-f", default="Extra/config.txt", type=str, help="file"
    )
    parser.add_argument("--monitoraddr", "-ma", type=str, help="monitor addr")
    args = parser.parse_args()
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    if args.sentype == "Ph":
        ph = Ph(args.file)
        sendInfo(ph)
    elif args.sentype == "Temperatura":
        temperature = Temperatura(args.file)
        sendInfo(temperature)
    elif args.sentype == "Oxigeno":
        oxygen = Oxigeno(args.file)
        sendInfo(oxygen)
