import pycom
import json
import os
from logger import *
from pysense import Pysense
from machine import Pin
import usocket as socket
import network

from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2, ALTITUDE, PRESSURE

logging = Logger('logging')
basicConfig(level=DEBUG)

btn = Pin('P14', mode=Pin.IN)

isBtnPressed = False
pycom.heartbeat(False)


logging = Logger('logging')
basicConfig(level=DEBUG)

# =====================NETWORK============================

ssid = 'SSID'
password = 'PASSWORD'

wlan = network.WLAN(mode=network.WLAN.STA)
wlan.connect(ssid, auth=(network.WLAN.WPA2, password))

while wlan.isconnected() == False:
    pass

logging.info('Connection successful')
print(wlan.ifconfig())


class Sensors:

    def __init__(self):
        self.py = Pysense()
        self.si = SI7006A20()
        self.lt = LTR329ALS01()
        self.li = LIS2HH12()
        self.mpp = MPL3115A2(self.py, mode=PRESSURE)

    def get_data_from_sensors(self):
        logging.info("Reading data from sensors")
        try:
            data = {
                "0": {
                    "Name": "Pressure", "Resource Definitions": {
                            str(self.mpp.get_pressure()["ID"]): self.mpp.get_pressure()
                    }
                },
                "1": {
                    "Name": "Temperature", "Resource Definitions": {
                            str(self.si.get_temperature()["ID"]): self.si.get_temperature()
                    }
                },
                "2": {
                    "Name": "Relative-Humidity", "Resource Definitions": {
                            str(self.si.get_humidity()["ID"]): self.si.get_humidity()
                    }
                },
                "3": {
                    "Name": "Acceleration", "Resource Definitions": {
                            str(self.li.get_acceleration_x()["ID"]): self.li.get_acceleration_x(),
                            str(self.li.get_acceleration_y()["ID"]): self.li.get_acceleration_y(),
                            str(self.li.get_acceleration_z()["ID"]): self.li.get_acceleration_z()
                    }
                },
                "4": {
                    "Name": "Luminosity", "Resource Definitions": {
                            str(self.lt.get_luminosity_blue()["ID"]): self.lt.get_luminosity_blue(),
                            str(self.lt.get_luminosity_red()["ID"]): self.lt.get_luminosity_red()
                    }
                },
            }
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
        s = socket.socket()
        s.bind(('', 80))
        s.listen(5)

        logging.info('Acception a connection...')
        conn, addr = s.accept()
        logging.info('Got a connection from %s' % str(addr))
        request = conn.recv(1024)
        logging.info('Content = %s' % str(request))

        response = self.get_json_sensors_data()

        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: application/json\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()


if __name__ == "__main__":
    while True:
        if (btn.value() == 0 and isBtnPressed == False):
            pycom.rgbled(0x00FF00)  # green
            print(Sensors().get_json_sensors_data())
            Sensors().send_sensors_data()
            isBtnPressed = True
        if (btn.value() == 1 and isBtnPressed == True):
            pycom.rgbled(0x000000)  # without light
            isBtnPressed = False
