import socket
import random
import time
import struct
import sys

WIN_STREAK = 5

def to_uint32(name: str) -> int:
    """Convert first 4 bytes of name into unsigned int (like C cast)."""
    name_bytes = name.encode("utf-8")[:4].ljust(4, b"\x00")
    return struct.unpack("<I", name_bytes)[0]

def greeting(conn): 

    conn.sendall(b"Greeting brother! First, what is your name?\n")
    conn.sendall(b">> ")
    name = conn.recv(1024).strip().decode(errors="ignore")

    return name
def handle_client(conn):
    #greeting step
    client = greeting(conn)

    wins = 0
    while wins < WIN_STREAK:
        conn.sendall(b"Your turn> ")
#        move = conn.recv(1024).strip().decode(errors="ignore").lower()

#        if move not in ["rock", "paper", "scissors"]:
#            conn.sendall(b"Invalid move. Use rock/paper/scissors.\n")
#            continue

#        server_move = ["rock", "paper", "scissors"][random.randint(0, 2)]
#        conn.sendall(f"Server plays {server_move}\n".encode())

        # result calculation
#        result = (["rock", "paper", "scissors"].index(move) -
#                  ["rock", "paper", "scissors"].index(server_move)) % 3

#        if result == 1:
#            wins += 1
#            conn.sendall(f"You win! ({wins}/{WIN_STREAK})\n".encode())
#        elif result == 2:
#            wins = 0
#            conn.sendall(b"You lose! Streak reset.\n")
#        else:
#            conn.sendall(b"Tie. Try again.\n")

#    conn.sendall(b"Congratulations! FLAG{dummy-flag}\n")
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

