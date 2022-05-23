import argparse
import getpass
import hashlib
import zmq
SYSTEM_PORT = 5554
SYSTEM_IP = "192.168.0.56"

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
    parser.add_argument("--user", "-u",required=True, type=str, help="Username")
    args = parser.parse_args()
    if user_validation(args.user):
        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        socket.connect(f"tcp://{SYSTEM_IP}:{SYSTEM_PORT}")
        

    else:
        print("Incorrect information")
