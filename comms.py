import socket


def connect(ip):
    host = ip #"192.168.1.119"
    port = 6274

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    return s

def disconnect(s):
    s.close()

def send_message(message, ip):
    s = connect(ip)
    s.send((message + "\n").encode())

def receive(s):
    return s.recv(1024).decode()


