import socket
import random
import time
import struct
import sys
import threading

client = []
lock = threading.lock()

def to_uint32(name: str) -> int:
    """Convert first 4 bytes of name into unsigned int (like C cast)."""
    name_bytes = name.encode("utf-8")[:4].ljust(4, b"\x00")
    return struct.unpack("<I", name_bytes)[0]

def greeting(conn): 

    conn.sendall(b"Greeting brother! First, what is your name?\n")
    name = conn.recv(1024).strip().decode(errors="ignore")

    conn.sendall(f"Hii {name}. Nice to meet you\n".encode())

    return name

def server_message(conn):
    pass

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

