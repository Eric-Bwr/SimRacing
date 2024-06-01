import time
import serial.tools.list_ports
from Util import *

ARDUINO_IN_MAX = 300


def runArduino(sharedData):
    arduino = serial.Serial(getArduinoPort(), 9600, write_timeout=0.1)
    print("Connected to Arduino.", flush=True)
    while True:
        clampedSpeed = clampValue(sharedData[KEY_SPEED], 0.0, ARDUINO_IN_MAX)
        mappedSpeed = mapValue(clampedSpeed, 0.0, ARDUINO_IN_MAX, 0.0, 100)
        arduino.write(f"{int(mappedSpeed)}\n".encode())
        time.sleep(0.1)


def getArduinoPort():
    while True:
        arduino_ports = [
            p.device
            for p in serial.tools.list_ports.comports()
            if "Arduino Micro" in p.description
        ]

        if arduino_ports:
            print("Found Sim-Racing setup, waiting a bit for it to load", flush=True)
            time.sleep(5)
            return arduino_ports[0]

        print("No Sim-Racing setup found, waiting...")

        time.sleep(1)
