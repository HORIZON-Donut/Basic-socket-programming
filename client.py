from pwn import *
import threading

def main():
    
    print("welcome. enter target ip and pont")

    ip = input("IP: ")
    port = int(input("Port: "))

    s = remote(ip, port)
    print(s.recvline())

    name = input()
    s.send(f"{name}\n".encode())

    while True:

        line = s.recvuntil(f"{name}: ".encode(), timeout=10)
        print(line.decode(), end="")

        if b": " in line:
            message = input()
            s.send(f"{message}\n".encode())

    s.close()

if __name__ == "__main__":
    main()
