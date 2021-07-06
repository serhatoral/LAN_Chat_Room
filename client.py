import socket
import threading

PORT = 5050
SERVER = "127.0.1.1"
ADDR = (SERVER , PORT)
FORMAT = 'utf-8'

nickname = input("Bir kullanıcı adı girin: ")

client = socket.socket(socket.AF_INET , socket.SOCK_STREAM) 
client.connect(ADDR) 

def send():
    while True:        
        message = f'[{nickname}]: {input()}'            
        client.send(message.encode(FORMAT))


def receive():
    while True:
        try:
            message = client.recv(1024).decode(FORMAT)
            if message == 'NICK?':  # Sunucuya kullanıcı adımızı yolluyoruz.
                client.send(nickname.encode(FORMAT))
            else:
                print(message)         

        except:
            print("Bağlantı hatası")
            client.close()
            break


receive_thread = threading.Thread(target=receive)
receive_thread.start()

send_thread = threading.Thread(target=send)
send_thread.start()
