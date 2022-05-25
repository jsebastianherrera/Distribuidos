import logging
from time import sleep
from Models.Ph import Ph
from Models.Oxigeno import Oxigeno
from Models.Temperatura import Temperatura
import argparse
import zmq


def sendInfo(generate):
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind(f"tcp://*:{args.port}")
    while True:
        sleep(args.time)
        valor = str(generate.generateValues())
        socket.send(args.sentype.encode() + b": " + valor.encode())
        logging.info(f"{args.port}: " + valor)
        print(args.sentype + ":" + valor)


if __name__ == "__main__":
    # signal.signal(signal.SIGINT, handler)
    parser = argparse.ArgumentParser(description="Publisher/suscriber implementation")
    parser.add_argument("--port", "-p", required=True, type=int, help="port number")
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
    args = parser.parse_args()
    logging.basicConfig(
        filename=f"DB/sen{args.sentype}.txt",
        level=logging.INFO,
        format="{asctime} {levelname:<8} {message}",
        style="{",
    )
    if args.sentype == "Ph":
        ph = Ph(args.file)
        sendInfo(ph)
    elif args.sentype == "Temperatura":
        temperature = Temperatura(args.file)
        sendInfo(temperature)
    elif args.sentype == "Oxigeno":
        oxygen = Oxigeno(args.file)
        sendInfo(oxygen)
