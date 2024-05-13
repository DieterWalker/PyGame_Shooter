import socket
from _thread import*
import sys

server = "192.168.1.112"
port = 8080

s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(5)
print("waiting for a connection, Server Started")

while True:
    client_socket, addr = s.accept()
    print("connected to:", addr)
    client_socket.send(bytes("Welcome to server", "utf-8"))