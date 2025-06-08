import socket

host = "192.168.1.119"
port = 6274

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

while True:
    msg = input("Send to ESP32: ")
    if msg.lower() == "exit":
        break
    s.send((msg + "\n").encode())
    data = s.recv(1024)
    print("Received:", data.decode())

s.close()
