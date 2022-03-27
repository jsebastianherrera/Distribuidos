from time import sleep
from Ph import Ph
from Oxigeno import Oxigeno
from Temperatura import Temperatura
import argparse
import zmq

parser = argparse.ArgumentParser(description="Publisher/suscriber implementation")
parser.add_argument("--port", "-p", default=5555, type=int, help="port number")
parser.add_argument(
    "--addr", "-a", default="127.0.0.1", type=str, help="Ip address IPV4"
)
parser.add_argument(
    "--type",
    "-t",
    default="Sensor",
    type=str,
    help="Type [Sensor,SistemaC,Oxigeno]",
    choices=["Sensor", "Monitor"],
)
parser.add_argument(
    "--sentype",
    "-s",
    default="Ph",
    type=str,
    help="Sensor type",
    choices=["Ph", "Temperatura", "Oxigeno"],
)
parser.add_argument("--time", "-tm", default=10, type=int, help="Time")
parser.add_argument("--file", "-f", default="config.txt", type=str, help="file")
args = parser.parse_args()
# -------------------------------------
context = zmq.Context()
socket = context.socket(zmq.PUB)
if args.type == "Sensor":
    if args.sentype == "Ph":
        ph = Ph(args.file)
        socket.bind(f"tcp://{args.addr}:{args.port}")
        while True:
            valor = str(ph.generateValues())
            socket.send(valor.encode())
            sleep(args.time)
    elif args.sentype == "Temperatura":
        temperature = Temperatura(args.file)
        socket.bind(f"tcp://{args.addr}:{args.port}")
        while True:
            valor = str(temperature.generateValues())
            socket.send(valor.encode()+ b'F')
            sleep(args.time)
    elif args.sentype == "Oxigeno":
        oxygen = Oxigeno(args.file)
        socket.bind(f"tcp://{args.addr}:{args.port}")
        while True:
            valor = str(oxygen.generateValues())
            socket.send(valor.encode()+ b'Mg/L')
            sleep(args.time)
