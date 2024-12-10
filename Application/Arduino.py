import time
import serial.tools.list_ports

SPEED_IN_MAX_KMH = 300
RPM_IN_MAX_PERC = 100

arduino = None


def initArduino():
    global arduino
    arduino = serial.Serial(getArduinoPort(), 9600, write_timeout=0.1)
    print("Connected to Arduino.", flush=True)


def setArduinoValues(speed, rpm):
    global arduino
    if arduino is None:
        print("Arduino not initialized.", flush=True)
        return

    clampedSpeed = clampValue(speed, 0.0, SPEED_IN_MAX_KMH)
    mappedSpeed = mapValue(clampedSpeed, 0.0, SPEED_IN_MAX_KMH, 0.0, 100)
    clampedRPM = clampValue(rpm, 0.0, RPM_IN_MAX_PERC)
    mappedRPM = mapValue(clampedRPM, 0.0, RPM_IN_MAX_PERC, 0.0, 100)
    arduino.write(f"{int(mappedSpeed)},{int(mappedRPM)}\n".encode())


def mapValue(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def clampValue(value, min_val, max_val):
    return min(max(value, min_val), max_val)


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

        time.sleep(1.0)
