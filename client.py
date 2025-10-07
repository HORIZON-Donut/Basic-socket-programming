from pwn import *
import threading

def recv_msg(s):
    while True:
        try:
            message = s.recvline(timeout = 1)

            if message:
                print(message.decode())
        except EOFError:
            break

        except:
            pass

def main():
    
    print("welcome. enter target ip and pont")

    ip = input("IP: ")
    port = int(input("Port: "))

    s = remote(ip, port)
    print(s.recvline())

    name = input()
    s.send(f"{name}\n".encode())

    threading.Thread(target=recv_msg, args=(s, ), daemon=True).start()

    while True:

        try:
            message = input()

            s.send(f"{message}\n".encode())

            if message.lower() == "exit":
                break

        except KeyboardInterrupt:
            s.send(b"exit\n")
            break

    s.close()

if __name__ == "__main__":
    main()
