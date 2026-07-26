import socket
import threading
import os
from datetime import datetime

host = '127.0.0.1' # localhost
port = 55555

if not os.path.exists("bans.txt"):
    open("bans.txt","w").close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []
muted_users = []
rooms = []

def broadcast(message):
    current_time = datetime.now().strftime('%H:%M:%S')
    message = f'[{current_time}] '.encode('ascii') + message
    for client in clients:
        client.send(message)

def room_broadcast(message, room):
    current_time = datetime.now().strftime('%H:%M:%S')
    message = f'[{current_time}] '.encode('ascii') + message
    for i in range(len(clients)):
        if rooms[i] == room:
            clients[i].send(message)

def handle(client):
    while True:
        try:
            msg = message = client.recv(1024)
            if msg.decode('ascii').startswith('KICK'):
                if nicknames[clients.index(client)] == 'admin':
                    name_to_kick = msg.decode('ascii')[5:]
                    kick_user(name_to_kick)
                else:
                    client.send('command was refused'.encode('ascii'))

            elif msg.decode('ascii').startswith('JOIN'):
                room = msg.decode('ascii')[5:].strip()
                if room == '':
                    client.send('Room name cannot be empty!'.encode('ascii'))
                else:
                    rooms[clients.index(client)] = room
                    client.send(f'Joined room {room}'.encode('ascii'))
                    nickname = nicknames[clients.index(client)]
                    room_broadcast(f'{nickname} joined the room.'.encode('ascii'), room)

            elif msg.decode('ascii') == 'ROOM':
                room = rooms[clients.index(client)]
                client.send(f'Current Room: {room}'.encode('ascii'))

            elif msg.decode('ascii') == 'ROOMS':
                room_names = []
                for room in rooms:
                    if room not in room_names:
                        room_names.append(room)
                room_list = 'Available Rooms:\n'
                for room in room_names:
                    room_list += room + '\n'
                client.send(room_list.encode('ascii'))
                    
            elif msg.decode('ascii').startswith('BAN'):
                if nicknames[clients.index(client)] == 'admin':
                    name_to_ban = msg.decode('ascii')[4:]
                    kick_user(name_to_ban)
                    with open('bans.txt', 'r') as f:
                        bans = f.readlines()
                    if name_to_ban + '\n' not in bans:
                        with open('bans.txt', 'a') as f:
                            f.write(f'{name_to_ban}\n')
                    print(f'{name_to_ban} was banned!')
                else:
                    client.send('command was refused'.encode('ascii'))

            elif msg.decode('ascii').startswith('MUTE'):
                if nicknames[clients.index(client)] == 'admin':
                    name_to_mute = msg.decode('ascii')[5:]
                    if name_to_mute in nicknames:
                        if name_to_mute not in muted_users:
                            muted_users.append(name_to_mute)
                            client.send(f'{name_to_mute} muted!'.encode('ascii'))
                    else:
                        client.send('User not found.'.encode('ascii'))
                else:
                    client.send('command was refused'.encode('ascii'))
                    
            elif msg.decode('ascii').startswith('UNMUTE'):
                if nicknames[clients.index(client)] == 'admin':
                    name_to_unmute = msg.decode('ascii')[7:]
                    if name_to_unmute in muted_users:
                        muted_users.remove(name_to_unmute)
                        client.send(f'{name_to_unmute} unmuted!'.encode('ascii'))
                else:
                    client.send('command was refused'.encode('ascii'))

            elif msg.decode('ascii').startswith('UNBAN'):
                if nicknames[clients.index(client)] == 'admin':
                    name_to_unban = msg.decode('ascii')[7:]
                    with open('bans.txt', 'r') as f:
                        bans = f.readlines()
                    with open('bans.txt', 'w') as f:
                        for ban in bans:
                            if ban.strip() != name_to_unban:
                                f.write(ban)
                    client.send(f'{name_to_unban} unbanned!'.encode('ascii'))
                else:
                    client.send('command was refused'.encode('ascii'))
            
            elif msg.decode('ascii').startswith('PM'):
                parts = msg.decode('ascii').split(' ', 2)
                if len(parts) < 3:
                    client.send('Usage: /pm <user> <message>'.encode('ascii'))
                    continue
                name = parts[1]
                private_msg = parts[2]
                if name in nicknames:
                    name_index = nicknames.index(name)
                    client_to_send = clients[name_index]
                    sender = nicknames[clients.index(client)]
                    client_to_send.send(f'[PM] {sender}: {private_msg}'.encode('ascii'))
                else:
                    client.send('User not found.'.encode('ascii'))

            elif msg.decode('ascii') == 'LIST':
                users = 'Online Users:\n'
                for nickname in nicknames:
                    users += nickname + '\n'
                client.send(users.encode('ascii'))

            elif msg.decode('ascii') == 'BANLIST':
                if nicknames[clients.index(client)] == 'admin':
                    ban_list = 'Ban List:\n'
                    with open('bans.txt', 'r') as f:
                        bans = f.readlines()
                    if len(bans) == 0:
                        client.send('Ban List is empty.'.encode('ascii'))
                    else:
                        ban_list = 'Ban List:\n'
                        for ban in bans:
                            ban_list += ban
                        client.send(ban_list.encode('ascii'))
                else:
                    client.send('command was refused'.encode('ascii'))

            elif nicknames[clients.index(client)] in muted_users:
                client.send('You are muted!'.encode('ascii'))

            else:
                room = rooms[clients.index(client)]
                room_broadcast(message, room) 


        except:
            if client in clients:
                index = clients.index(client)
                clients.remove(client)
                nickname = nicknames.pop(index)
                rooms.pop(index)
                client.close()
                broadcast(f'{nickname} left the chat!'.encode('ascii'))
                break

def receive():
    while True:
        client, address = server.accept()
        print(f"connected with {str(address)}")

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        if nickname in nicknames:
            client.send('Nickname already exists.'.encode('ascii'))
            client.close()
            continue

        with open('bans.txt', 'r') as f:
            bans = f.readlines()
        if nickname+'\n' in bans:
            client.send('BAN'.encode('ascii'))
            client.close()
            continue

        if nickname == 'admin':
            client.send('PASS'.encode('ascii'))
            password = client.recv(1024).decode('ascii')
            if password != 'adminpass':
                client.send('REFUSE'.encode('ascii'))
                client.close()
                continue

        nicknames.append(nickname)
        clients.append(client)
        rooms.append('General')

        print(f'Nickname of the client is {nickname}')
        broadcast(f'{nickname} join the chat'.encode('ascii'))
        client.send('connected to the server'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

def kick_user(name):
    if name in nicknames:
        name_index = nicknames.index(name)
        client_to_kick = clients[name_index]
        clients.remove(client_to_kick)
        nickname = nicknames.pop(name_index)
        rooms.pop(name_index)
        client_to_kick.send('You were kick by admin!'.encode('ascii'))
        client_to_kick.close()
        broadcast(f'{nickname} was kick by admin!'.encode('ascii'))

print("Server is listening...") 
receive()
