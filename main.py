import pycom
import json
import os
from logger import *
from pysense import Pysense
from machine import Pin

from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2, ALTITUDE, PRESSURE

logging = Logger('logging')
py = Pysense()
si = SI7006A20(py)
lt = LTR329ALS01(py)
li = LIS2HH12(py)
mpp = MPL3115A2(py, mode=PRESSURE)

btn = Pin('P14', mode=Pin.IN)

isBtnPressed = False
pycom.heartbeat(False)
basicConfig(level=DEBUG)


def writeData(file="dataBase.json"):
    logging.info('Opening file ' + file + '...')
    try:
        with open(file, 'r+') as f:
            logging.info("Receiving sensor's data and writing to the file...")
            fileSize = os.stat(file)[6]
            if(fileSize == 0):
                f.write(json.dumps([{"Pressure": str(mpp.pressure()), "Temperature": str(si.temperature()), "Relative-Humidity": str(si.humidity()),
                                     "Acceleration": str(li.acceleration()), "Luminosity": str(lt.light())}]))
            else:
                f.seek(fileSize - 1)
                f.write(',\n')
                f.write(json.dumps({"Pressure": str(mpp.pressure()), "Temperature": str(si.temperature()), "Relative-Humidity": str(si.humidity()),
                                    "Acceleration": str(li.acceleration()), "Luminosity": str(lt.light())}))
                f.write('\n]')
    except:
        logging.error('File cannot be opened.')
    else:
        logging.info('Data has been successfully written to the file ' + file)


def checkButton(isBtnPressed):
    if (btn.value() == 0 and isBtnPressed == False):
        pycom.rgbled(0x00FF00)  # green
        writeData("dataBase.json")
        isBtnPressed = True
    if (btn.value() == 1 and isBtnPressed == True):
        pycom.rgbled(0x000000)  # without light
        isBtnPressed = False


while True:
    checkButton(isBtnPressed)
