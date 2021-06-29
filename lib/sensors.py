import json
import os
from logger import *
from pysense import Pysense
import socket

from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2, ALTITUDE, PRESSURE

logging = Logger('logging')
basicConfig(level=DEBUG)


class Sensors:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.py = Pysense()
        self.si = SI7006A20()
        self.lt = LTR329ALS01()
        self.li = LIS2HH12()
        self.mpp = MPL3115A2(self.py, mode=PRESSURE)

    def get_data_from_sensors(self):
        logging.info("Reading data from sensors")
        try:
            sens = [self.mpp.get_pressure(), self.si.get_temperature(
            ), self.si.get_humidity(), self.li.get_acceleration(), self.lt.get_luminosity()]
            data = {}
            for i in range(0, 4):
                data[str(i)] = sens[i]
            return data

        except:
            logging.error("Data cannot be read")
        else:
            logging.info("Data reading completed")
            return data

    def get_json_sensors_data(self):
        logging.info("Transforming data from sensors to json format")
        try:
            json_data = json.dumps(self.get_data_from_sensors())
        except:
            logging.error("Data cannot be transform to json format")
        else:
            logging.info("Data transforming completed")
            return json_data

    def send_sensors_data(self):
        json_data = self.get_json_sensors_data()
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logging.info('Connection to %s' % str((self.host, self.port)))
        try:
            client_sock.connect((self.host, self.port))
        except OSError:
            logging.error("System error - unable to connect")
        else:
            logging.info('Got a connection from %s' %
                         str((self.host, self.port)))
            logging.info('Sending data ')
            client_sock.sendall(json_data.encode(encoding='utf-8'))
            client_sock.close()
            logging.info('Data is received')
