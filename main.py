from pysense import Pysense
import machine
import os
import time
import pycom
import sys
from machine import Pin

btn = Pin('P14', mode=Pin.IN)

pycom.heartbeat(False)

while True:
    if (btn.value() == 0):
        pycom.rgbled(0x0000FF)  # Голубой
    if (btn.value() == 1):
        pycom.rgbled(0x00FF00)  # Зеленый
    if (btn.value() != 0 and btn.value() != 1):
        pycom.rgbled(0xFF0000) # Красный 

#=============================FILES================================

with open("dataBase.txt",'a') as f:
   f.write('{\n"address": "192.168.4.1",\n "username": "micro",\n}\n')

#============================SENSORS===============================

# from pysense import Pysense
# from LIS2HH12 import LIS2HH12
# from SI7006A20 import SI7006A20
# from LTR329ALS01 import LTR329ALS01
# from MPL3115A2 import MPL3115A2, ALTITUDE, PRESSURE

# py = Pysense()
# # Returns height in meters. Mode may also be set to PRESSURE, returning a value in Pascals
# mp = MPL3115A2(py, mode=ALTITUDE)
# si = SI7006A20(py)
# lt = LTR329ALS01(py)
# li = LIS2HH12(py)

# print("MPL3115A2 temperature: " + str(mp.temperature()))
# print("Altitude: " + str(mp.altitude()))
# # Returns pressure in Pa. Mode may also be set to ALTITUDE, returning a value in meters
# mpp = MPL3115A2(py, mode=PRESSURE)
# print("Pressure: " + str(mpp.pressure()))

# print("Temperature: " + str(si.temperature()) +
#       " deg C and Relative Humidity: " + str(si.humidity()) + " %RH")
# print("Dew point: " + str(si.dew_point()) + " deg C")
# t_ambient = 24.4
# print("Humidity Ambient for " + str(t_ambient) +
#       " deg C is " + str(si.humid_ambient(t_ambient)) + "%RH")

# print("Light (channel Blue lux, channel Red lux): " + str(lt.light()))

# print("Acceleration: " + str(li.acceleration()))
# print("Roll: " + str(li.roll()))
# print("Pitch: " + str(li.pitch()))

# print("Battery voltage: " + str(py.read_battery_voltage()))
