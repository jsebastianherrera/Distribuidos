from time import sleep
from Ph import Ph
from Oxigeno import Oxigeno
from Temperatura import Temperatura
import argparse
import zmq

def sendInfo(type: str, generate):
    socket.bind(f"tcp://{args.addr}:{args.port}")
    while True:
        sleep(args.time)
        valor = str(generate.generateValues())
        socket.send(type.encode() + valor.encode())
        print(type.upper() + valor)


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
parser.add_argument("--file", "-f", default="config.txt", type=str, help="file")
parser.add_argument("--monitoraddr", "-ma", type=str, help="monitor addr")
args = parser.parse_args()


def sendInfo(generate):
    socket.bind(f"tcp://{args.addr}:{args.port}")
    while True:
        sleep(args.time)
        valor = str(generate.generateValues())
        socket.send(args.sentype.encode() + b": " + valor.encode())
        print(args.sentype + ":" + valor)


# -------------------------------------
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
