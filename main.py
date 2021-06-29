import pycom
from machine import Pin
from network_conn import Network
from sensors import Sensors

net = Network('Valera', '8542482val')
sens = Sensors("192.168.100.13", 5001)
btn = Pin('P14', mode=Pin.IN)

isBtnPressed = False
pycom.heartbeat(False)

net.connect()

if __name__ == "__main__":
    while True:
        if (btn.value() == 0 and isBtnPressed == False):
            pycom.rgbled(0x00FF00)  # green
            isBtnPressed = True
        if (btn.value() == 1 and isBtnPressed == True):
            pycom.rgbled(0x000000)  # without light
            sens.send_sensors_data()
            isBtnPressed = False
