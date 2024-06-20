import threading 
import socket
import sys
import time

# ホストとポートの設定
host = ''
port = 9000
local_address = (host, port) 

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

tello_address = ('192.168.10.1', 8889)

sock.bind(local_address)

def receive_messages():
    while True: 
        try:
            data, server = sock.recvfrom(1518)
            print(f"Received message: {data.decode('utf-8')}")
        except Exception:
            print('\n終了します。\n')
            break

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

while True: 
    command_message = "command".encode("utf-8") 
    sock.sendto(command_message, tello_address)
    print("Telloと通信を開始しました。")

    # "takeoff"など詳しくはcommands参照
    try:
        user_command = input("Telloに送る指示コマンドを入力してください： ")
        if not user_command:
            print("空のコマンドが入力されました。終了します。")
            break  

        command_message = user_command.encode("utf-8") 
        sock.sendto(command_message, tello_address)

    except KeyboardInterrupt:
        print("終了します。")
        sock.close()  
        break
