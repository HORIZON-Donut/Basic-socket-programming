from pwn import *

s = remote("localhost", 1234)
print(s.recvline())

name = input()
s.send(f"{name}\n".encode())

while True:

    print(s.recvline())

    if b": " in line:
        message = input()
        s.send(f"{message}\n".encode())

s.close()

