# TCP Multi-Client Chat Application

A multi-client TCP chat application built with Python using Socket Programming and Threading. The project supports real-time messaging, chat rooms, private messaging, and administrator management features.

---

## Features

### User Features

- Multi-client TCP communication
- Real-time public messaging
- Private messaging (`/pm`)
- Chat rooms (`/join`)
- View current room (`/room`)
- View available rooms (`/rooms`)
- Online user list (`/list`)
- Timestamped messages

### Administrator Features

- Kick users
- Ban / Unban users
- Mute / Unmute users
- View banned users (`/banlist`)

---

## Technologies

- Python
- Socket Programming
- TCP/IP
- Multithreading


## Project Structure

```
TCP-ChatRoom/
│
├── server.py
├── client.py
├── bans.txt
└── README.md
```

---

## How to Run

### Start the Server

```bash
python server.py
```

### Start a Client

```bash
python client.py
```

Run multiple clients in separate terminals to test the application.

---

## Available Commands

### User Commands

| Command | Description |
|----------|-------------|
| `/pm <user> <message>` | Send a private message |
| `/join <room>` | Join or create a chat room |
| `/room` | Show current room |
| `/rooms` | Show all available rooms |
| `/list` | Show online users |

### Admin Commands

| Command | Description |
|----------|-------------|
| `/kick <user>` | Disconnect a user |
| `/ban <user>` | Ban a user |
| `/unban <user>` | Remove a ban |
| `/mute <user>` | Mute a user |
| `/unmute <user>` | Unmute a user |
| `/banlist` | Show banned users |

---

## Screenshots

### Network Architecture

*(Insert topology or architecture screenshot)*

### Server Console

*(Insert screenshot)*

### Client Chat

*(Insert screenshot)*

### Chat Rooms

*(Insert screenshot)*

### Administrator Commands

*(Insert screenshot)*

---

## Skills Demonstrated

- TCP Socket Programming
- Multi-threaded Server Development
- Client-Server Architecture
- Network Communication
- Command Parsing
- User Session Management
- Basic Access Control
- Configuration Management

---

## Future Improvements

- GUI Client (Tkinter)
- SSL/TLS Encryption
- Rate Limiting
- File Transfer
- Server Logging

---

## License

This project is intended for educational purposes.
