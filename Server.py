import socket
import threading
import pickle
from time import sleep
import select
import logging
from Logs.log_conf import logger, full_file_path
import requests
from requests.exceptions import HTTPError, ConnectionError

# Define Logger
file_handler = logging.FileHandler(f"{full_file_path}_Server.log")
file_handler.setLevel(logging.DEBUG)
logger.addHandler(file_handler)

# Server&Api parameters
HEADER = 64
SOCKET_PORT  = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, SOCKET_PORT)
FORMAT = "utf-8"
API_PORT = 5000
API_URL = f"http://127.0.0.1:{API_PORT}"

# Define messages
ID = f"{ADDR}"

# Connect to the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def update_endpoint(data, update):
    '''
        Updates or creates new object representing robot
    '''
    try:
        url = f"{API_URL}/api/courses"  
        if not update:
            response = requests.post(url, json=data)
            update = True
        else:
            url += f"/{data['name']}"
            response = requests.put(url, json=data)
        response.raise_for_status()
        logger.info(f"Response code: {response.status_code}")
        logger.info(f"Response json: {response.json()}")   
        return update
    except HTTPError as he:
        if response.status_code == 500:
            logger.error(f"HTTPError: Internal server error. Check if multiple client modify same robot object in API..... {he}")
        logger.error(f"HTTPError: {he}")
    except ConnectionError as ce:
        logger.error(f"ConnectionError: Failed to establish a connection to the server: {ce}")
    except Exception as e:
        logger.error(f"Exception: {e}") 

def delete_endpoint(data):
    '''
        Deletes object representing robot
    '''
    try:
        url = f"{API_URL}/api/courses/{data['name']}"
        response = requests.delete(url)
        response.raise_for_status()
        logger.info(f"Response code: {response.status_code}")
    except HTTPError as he:
        if response.status_code == 500:
            logger.error(f"HTTPError: Internal server error. Check if multiple client modify same robot object in API..... {he}")
        logger.error(f"HTTPError: {he}")
    except ConnectionError as ce:
        logger.error(f"ConnectionError: Failed to establish a connection to the server: {ce}")
    except Exception as e:
        logger.error(f"Exception: {e}")

def handle_client(conn, addr):
    '''
        Handles single client connection
    '''
    logger.info(f"[NEW CONNECTION] {addr} connected.")
    connected = True  # flag to keep the connection alive
    update = False  # flag to update or create new object representing robot

    while connected:
        sleep(0.001)
        try:
            ready = select.select([conn], [], [], 1) # waits for the message for 1 second
            if ready[0]:  
                msg_length = conn.recv(HEADER).decode(FORMAT)
                if msg_length:  # if message is not empty read the message and send acknowledgment
                    msg_length = int(msg_length)
                    msg = conn.recv(msg_length)  # read the message
                    d = pickle.loads(msg)
                    logger.info(f"from: [{addr}] Received object: {d}")
                    conn.send(ID.encode(FORMAT)) # send acknowledgment
                    update = update_endpoint(d, update)
            conn.send("Heartbeat".encode(FORMAT)) # send heartbeat
            logger.info(f"Sent heartbeat to: [{addr}]")
        except BrokenPipeError:
            logger.error(f"[ERROR] BrokenPipeError occurred for client {addr}")
            connected = False
            delete_endpoint(d)
    conn.close()
    logger.info(f"[CONNECTION CLOSED] Connection with {addr} closed.")

def start():
    try:
        server.listen()
        logger.info(f"[LISTENING] Server is listening on {SERVER}")
        while True:
            conn, addr = server.accept()  # waits there until new connection is formed
            thread = threading.Thread(target=handle_client, args=(conn, addr))  # create new thread for each client
            thread.start()
            logger.info(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
    except KeyboardInterrupt:
        logger.error(' CTRL+C')

logger.info("[STARTING] server is starting...")
start()

#CHANGELOG
# 1. Need to add more specific info about heartbeat
# 2. Need to add more specific info about exception handling
# 3. Not unit test written yet
# 4. Need to setup Firewall to allow connection for all clients
