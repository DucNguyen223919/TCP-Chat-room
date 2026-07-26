import socket
import threading

nickname = input("Choose a nickname:")
if nickname == 'admin':
    password = input("Enter password for admin: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

stop_thread = False

def receive():
    while True:
        global stop_thread
        if stop_thread:
            break
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
                next_message = client.recv(1024).decode('ascii')
                if next_message == 'PASS':
                    client.send(password.encode('ascii'))
                    if client.recv(1024).decode('ascii') == 'REFUSE':
                        print("Connection was refused. Wrong password!")
                        stop_thread = True
                elif next_message == 'BAN':
                    print('Connection refused because of ban!')
                    client.close()
                    stop_thread = True
            else:
                print(message)
        except:
            print("An error occured!")
            client.close()
            break

def write():
    while True:
        if stop_thread:
            break
        message = f'{nickname}: {input("")}'
        if message[len(nickname)+2:].startswith('/'):
            if message[len(nickname)+2:].startswith('/pm'):
                client.send(f'PM {message[len(nickname)+2+4:]}'.encode('ascii'))
            elif message[len(nickname)+2:].startswith('/join'):
                client.send(f'JOIN {message[len(nickname)+2+6:]}'.encode('ascii'))
            elif message[len(nickname)+2:].startswith('/room'):
                client.send('ROOM'.encode('ascii'))
            elif message[len(nickname)+2:].startswith('/rooms'):
                client.send('ROOMS'.encode('ascii'))
            elif message[len(nickname)+2:].startswith('/list'):
                client.send('LIST'.encode('ascii'))
            elif message[len(nickname)+2:].startswith('/banlist'):
                client.send('BANLIST'.encode('ascii'))

            elif nickname == 'admin':
                if message[len(nickname)+2:].startswith('/kick'):
                    client.send(f'KICK {message[len(nickname)+2+6:]}'.encode('ascii'))
                elif message[len(nickname)+2:].startswith('/mute'):
                    client.send(f'MUTE {message[len(nickname)+2+6:]}'.encode('ascii'))
                elif message[len(nickname)+2:].startswith('/unmute'):
                    client.send(f'UNMUTE {message[len(nickname)+2+8:]}'.encode('ascii'))
                elif message[len(nickname)+2:].startswith('/unban'):
                    client.send(f'UNBAN {message[len(nickname)+2+7:]}'.encode('ascii'))
                elif message[len(nickname)+2:].startswith('/ban'):
                    client.send(f'BAN {message[len(nickname)+2+5:]}'.encode('ascii'))
            else:
                print("Cmd only exc by admin")

        else:
            client.send(message.encode('ascii'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()