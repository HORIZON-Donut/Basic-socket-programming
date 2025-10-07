import socket
import random
import time
import struct
import sys
import threading

client = []
lock = threading.Lock()

def to_uint32(name: str) -> int:
    """Convert first 4 bytes of name into unsigned int (like C cast)."""
    name_bytes = name.encode("utf-8")[:4].ljust(4, b"\x00")
    return struct.unpack("<I", name_bytes)[0]

def greeting(conn): 

    conn.sendall(b"Well come to the chat. First, enter your name?\n")
    name = conn.recv(1024).strip().decode(errors="ignore")
    message = f"New chatter: {name} Have enter the chat.\n".encode()

    print(f"{name} have enter the chat\n");
    brocast(message, conn)

    return name

def brocast(message, sernder=None):
    
    with lock:
        for client in clients:
            if client != sender:
                try:
                    client.sendall(message)

                except:
                    client.close()
                    clients.remove(client)

def handle_client(conn):
    #greeting step
    client = greeting(conn)

    while True:
        conn.sendall(f"{client}: ".encode())
        message = conn.recv(1024).strip().decode()

        print(message)

        if message.lower() == "exit":
            conn.sendall(f"Bye, have a great day\n".encode())

            break

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
        while True:
            conn, addr = s.accept()
            print(f"[+] Connection from {addr}")
            handle_client(conn)

if __name__ == "__main__":
    main()

