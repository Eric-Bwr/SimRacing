import struct
import socket
import time

from Util import *

UDP_IP = "127.0.0.1"
UDP_PORT = 30500

jumps = {
    's32': 4,  # Signed 32bit int, 4 bytes of size
    'u32': 4,  # Unsigned 32bit int
    'f32': 4,  # Floating point 32bit
    'u16': 2,  # Unsigned 16bit int
    'u8': 1,  # Unsigned 8bit int
    's8': 1,  # Signed 8bit int
    'hzn': 12  # Unknown, 12 bytes of.. something
}

dataTypes = {}
with open('Formats/FH5.txt', 'r') as f:
    print("Reading format data")
    lines = f.read().split('\n')
    for line in lines:
        dataTypes[line.split()[1]] = line.split()[0]


def getData(data):
    return_dict = {}

    passed_data = data

    for i in dataTypes:
        d_type = dataTypes[i]
        jump = jumps[d_type]
        current = passed_data[:jump]

        decoded = 0
        if d_type == 's32':
            decoded = int.from_bytes(current, byteorder='little', signed=True)
        elif d_type == 'u32':
            decoded = int.from_bytes(current, byteorder='little', signed=False)
        elif d_type == 'f32':
            decoded = struct.unpack('f', current)[0]
        elif d_type == 'u16':
            decoded = struct.unpack('H', current)[0]
        elif d_type == 'u8':
            decoded = struct.unpack('B', current)[0]
        elif d_type == 's8':
            decoded = struct.unpack('b', current)[0]

        return_dict[i] = decoded

        passed_data = passed_data[jump:]
    return return_dict


def updateTelemetryData(sharedData):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    while True:
        data, addr = sock.recvfrom(1500)
        parsedData = getData(data)
        sharedData[KEY_IS_RACE_ON] = bool(parsedData.get("IsRaceOn", 0))
        sharedData[KEY_SPEED] = parsedData.get("Speed", 0) * 3.6
        gear = parsedData.get("Gear", 0)
        if gear == 11:
            sharedData[KEY_GEAR] = "N"
        elif gear == 0:
            sharedData[KEY_GEAR] = "R"
        else:
            sharedData[KEY_GEAR] = str(gear)
        sharedData[KEY_ENGINE_RPM] = parsedData.get("CurrentEngineRpm", 0)
        sharedData[KEY_ENGINE_RPM_MAX] = parsedData.get("EngineMaxRpm", 0)
        if sharedData[KEY_ENGINE_RPM_MAX] == 0.0:
            sharedData[KEY_ENGINE_RPM_PERC] = 0.0
        else:
            sharedData[KEY_ENGINE_RPM_PERC] = (sharedData[KEY_ENGINE_RPM] / sharedData[KEY_ENGINE_RPM_MAX])
