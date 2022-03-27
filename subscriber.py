import argparse
from email import message
from time import sleep
import zmq
parser=argparse.ArgumentParser(description="Publisher/suscriber implementation")
parser.add_argument('--port','-p',default=5555,type=int,help='port number')
parser.add_argument('--addr','-a',default='127.0.0.1',type=str,help='Ip address IPV4')
args=parser.parse_args()
#-------------------------------------
context=zmq.Context()
socket=context.socket(zmq.SUB)
socket.connect(f'tcp://{args.addr}:{args.port}')
socket.setsockopt_string(zmq.SUBSCRIBE,'')
while True:
    message = socket.recv()
    print(message.decode())