import socket
from logger import *

logging = Logger('logging')
basicConfig(level=DEBUG)

HOST = '0.0.0.0'
PORT = 5001

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    logging.info('Acception a connection...')
    conn, addr = s.accept()
    with conn:
        logging.info('Connected by', addr)
        data = conn.recv(1024)
        logging.info("""Writing sensor's data to the file...""")
        with open('sensors_data.json', 'br+') as f:
            f.write(data)
        print('Writing is done')
