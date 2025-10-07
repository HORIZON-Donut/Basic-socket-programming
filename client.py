from pwn import *

s = remote("localhost", 1234)
print(s.recvline())

name = input()
s.send(f"{name}\n".encode())

while True:

    line = s.recvline(timeout=5)
    print(line.decode(), end="")

    if b": " in line:
        message = input()
        s.send(f"{message}\n".encode())

s.close()

