import socket
import struct
import time
import serial.tools.list_ports

UDP_IP = "127.0.0.1"
UDP_PORT = 30500

data_types = {}
with open('data_format_fh5.txt', 'r') as f:
    lines = f.read().split('\n')
    for line in lines:
        data_types[line.split()[1]] = line.split()[0]

jumps = {
    's32': 4,  # Signed 32bit int, 4 bytes of size
    'u32': 4,  # Unsigned 32bit int
    'f32': 4,  # Floating point 32bit
    'u16': 2,  # Unsigned 16bit int
    'u8': 1,   # Unsigned 8bit int
    's8': 1,   # Signed 8bit int
    'hzn': 12  # Unknown, 12 bytes of.. something
}

def get_data(data):
    return_dict = {}

    passed_data = data
    
    for i in data_types:
        d_type = data_types[i]
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

def get_arduino_port():
    start_time = time.time()
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

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

ser = serial.Serial(get_arduino_port(), 9600, write_timeout=0.1) 

print("Connected.", flush=True)

def map_value(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def clamp_value(value, min_val, max_val):
    return min(max(value, min_val), max_val)

average_speed = 0
count = 0
interval_start_time = time.time()

try:
    while True:
        data, addr = sock.recvfrom(1500)
        returned_data = get_data(data)
    
        speed_kph = returned_data.get('Speed', 0) * 3.6
        
        average_speed += speed_kph
        count += 1
        
        current_time = time.time()

        if current_time - interval_start_time >= 0.1:
            average_speed /= count
            mapped_speed = map_value(average_speed, 0.0, 300.0, 0.0, 100.0)
            mapped_speed = clamp_value(mapped_speed, 0.0, 100.0)
            mapped_speed = int(mapped_speed)
            average_speed = int(average_speed)
            ser.write(f"{mapped_speed}\n".encode()) 
            print("Average speed:", average_speed, "Mapped speed:", mapped_speed)
            average_speed = 0
            count = 0
            interval_start_time = time.time()
        time.sleep(0.001)
            
except KeyboardInterrupt:
    ser.write(f"{0}".encode()) 
    print("Sending 0 on exit");
ser.close()

