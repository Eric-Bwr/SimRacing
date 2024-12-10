import struct
import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 30500

jumps = {
    's32': 4,  # Signed 32bit int, 4 bytes of size
    'u32': 4,  # Unsigned 32bit int
    'f32': 4,  # Floating point 32bit
    'u16': 2,  # Unsigned 16bit int
    'u8': 1,  # Unsigned 8bit int
    's8': 1,  # Signed 8bit int
    'hzn': 12  # Unknown, 12 bytes of something
}

dataTypes = {}
with open('formats/FH5.txt', 'r') as f:
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


def updateTelemetryData(cb):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    while True:
        data, addr = sock.recvfrom(1500)
        parsedData = getData(data)

        isRaceOn = bool(parsedData.get("IsRaceOn", 0))

        speed = parsedData.get("Speed", 0) * 3.6

        gear = parsedData.get("Gear", 0)
        if gear == 11:
            gearString = "N"
        elif gear == 0:
            gearString = "R"
        else:
            gearString = str(gear)

        rpm = parsedData.get("CurrentEngineRpm", 0)
        rpmMax = parsedData.get("EngineMaxRpm", 0)
        if rpmMax == 0.0:
            rpmNorm = 0.0
        else:
            rpmNorm = rpm / rpmMax

        cb(isRaceOn, speed, gearString, rpmNorm)
