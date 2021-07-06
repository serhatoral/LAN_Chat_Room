# - *- coding: utf- 8 - *-
import socket
import threading

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())  # host isminden local ip'yi getirir.
ADDR = (SERVER , PORT)
FORMAT = 'utf-8'

clients = []
nicknames = []


server = socket.socket(socket.AF_INET , socket.SOCK_STREAM)   
server.bind(ADDR) 


def broadcast(message, clnt):
     
    for client in clients:
        if client != clnt:
            client.send(message)
        


def handle_client(connection):
       
    while True:
        try:
            message = connection.recv(1024) # client dan mesaj alıyoruz.                        
            broadcast(message,connection)             
                                          
        except: 
            
            index = clients.index(connection)
            clients.remove(connection)
            connection.close()

            nickname = nicknames[index]
            print(f"{nickname} odadan ayrıldı!") # sunucuda mesajı yazdırıyoruz
            broadcast(f'{nickname} odadan ayrıldı'.encode(FORMAT),connection) # sunucuya bağlı tüm istemcilerde mesajı yayınlıyoruz.
            nicknames.remove(nickname)
            break
            
        

def start():
    server.listen()
    print("Sunucu dinleniyor...")
    while  True:
        connection, address = server.accept()
        print(f"{str(address)} ile bağlantı sağlandı.")

        connection.send('NICK?'.encode(FORMAT)) # Kullanıcıdan kullanıcı adını istiyoruz.
        nickname= connection.recv(1024).decode(FORMAT)  #Kullanıcının yolladığı veriyi alıyoruz.
        nicknames.append(nickname)
        clients.append(connection)
        print(f"{str(address)}\'nin kullanıcı adı {nickname}\'dir.")               
        connection.send('Sunucuya başarılı bir şekilde bağlandınız.'.encode(FORMAT))
        broadcast(f'{nickname} odaya katıldı'.encode(FORMAT),connection) 
        

        thread = threading.Thread(target=handle_client, args=(connection,))
        thread.start()
        print(f"Aktif Bağlantı sayısı: {threading.activeCount()-1}")


print("Sunucu başlatılıyor...")
start()