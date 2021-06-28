import network
from logger import *

logging = Logger('logging')
basicConfig(level=DEBUG)


class Network:

    def __init__(self, ssid, password):
        self.ssid = ssid
        self.password = password

    def connect(self):
        wlan = network.WLAN(mode=network.WLAN.STA)
        wlan.connect(self.ssid, auth=(network.WLAN.WPA2, self.password))

        while wlan.isconnected() == False:
            pass

        logging.info('Connection successful')
        print(wlan.ifconfig())
