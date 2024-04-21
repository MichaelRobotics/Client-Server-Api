import socket
import pickle
from time import sleep
import schedule
import traceback
import logging
from Logs.log_conf import logger, full_file_path

# Define Logger
file_handler = logging.FileHandler(f"{full_file_path}_Client.log")
file_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)

# Server parameters
HEADER = 64
PORT  = 5050
SERVER = socket.gethostbyname(socket.gethostname()) # !!!MODIFY WHEN SERVER IS REMOTE!!!
ADDR = (SERVER, PORT)
FORMAT = "utf-8"

# Define messages
IP = "127.0.1.1"
ID = "RobotOne"
DICT = {"IP": IP, "name": ID}

# Prepare messages for sending
message = pickle.dumps(DICT)

# Connect to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
logger.info(f"[CONNECTED] Connected to {SERVER}")


def send(message):
    '''
        Sends message to the server
    '''
    try:
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        if msg_length > HEADER:
            raise Exception("Message length exceeds header length")
        send_length += b" " * (HEADER - len(send_length))
        client.send(send_length)
        client.send(message)
        logger.info(f"obj {DICT} send succesfuly to: {client.recv(2048).decode(FORMAT)}")

    except Exception as e: 
        client.close()
        logger.error(f"Exception: An unexpected error occurred: {e}")
        logger.error(traceback.print_exc())

# Schedule frequency of sending messages
schedule.every(10).seconds.do(send, message)

# Receive heartbeat messages from the server and schedule sending messages
while True:
    try:
        sleep(0.001)
        logger.info(f"Received: {client.recv(2048).decode(FORMAT)}")
        schedule.run_pending()

    except OSError as e:
        client.close()
        logger.error(f"OSError: [Errno {e.errno}] {e.strerror}.")
        logger.error(traceback.print_exc())
        break

#CHANGELOG
# 1. Need to add more specific info about heartbeat
# 2. Need to add more specific info about exception handling
# 3. Not unit test written yet
# 4. Need to setup Firewall and automatic IP get from machine on Client