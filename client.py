from pwn import *

s = remote("localhost", 1234)
# s.send(b"hello\n")
# print(s.recvline())
# s.close()

while True:

    print(s.recvline())

    message = input()

    s.send(b"{message}\n)

s.close()

