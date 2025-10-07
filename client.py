from pwn import *

s = remote("localhost", 1234)
# s.send(b"hello\n")
# print(s.recvline())
# s.close()

# Receive the greeting
print(s.recvuntil(b"Your name> "))
s.send(b"horizon\n")

while True:
    line = s.recvuntil(b"> ", timeout=5)
    print(line.decode(), end="")

s.close()

