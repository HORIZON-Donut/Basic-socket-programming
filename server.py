import socket
import random
import time
import struct
import sys
import threading

clients = []
lock = threading.Lock()
is_server_active = 0

def to_uint32(name: str) -> int:
    """Convert first 4 bytes of name into unsigned int (like C cast)."""
    name_bytes = name.encode("utf-8")[:4].ljust(4, b"\x00")
    return struct.unpack("<I", name_bytes)[0]

def new_client(conn):
    with lock:
        clients.append(conn)

def greeting(conn): 

    conn.sendall(b"Well come to the chat. First, enter your name?\n")
    name = conn.recv(1024).strip().decode(errors="ignore")
    message = f"New chatter: {name} Have enter the chat.\n".encode()

    print(f"{name} have enter the chat\n");
    brocast(message, conn)

    new_client(conn)

    return name

def brocast(message, sender=None):
    
    with lock:
        for client in clients:
            if client != sender:
                try:
                    client.sendall(message)

                except:
                    client.close()
                    clients.remove(client)

def exit_point(conn, name):
    with lock:
        if conn in clients:
            clients.remove(conn)

        conn.close()
        message = f"{name} have leave the chat\n".encode()
        print(message.decode())

        brocast(message)

def handle_client(conn):
    #greeting step
    client = greeting(conn)

    while is_server_active == 0:
        data = conn.recv(1024)

        if not data:
            break

        message = data.strip().decode()

        if message.lower() == "exit":
            exit_point(conn, client)
            break

        msg = f"{client}: {message}\n".encode()
        print(msg.decode())

        brocast(msg, conn)

    conn.close()

def main():
    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} <port>")
        sys.exit(1)

    PORT = int(sys.argv[1])
    HOST = "0.0.0.0"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[*] Python target running on {HOST}:{PORT}")
        try:
            while True:
                conn, addr = s.accept()
                print(f"[+] Connection from {addr}")
                thread = threading.Thread(target=handle_client, args=(conn, ))
                thread.start()

        except KeyboardInterrupt:
            print("\n[!] Server shutdown")
            is_server_active = 1
            s.close()

if __name__ == "__main__":
    main()

