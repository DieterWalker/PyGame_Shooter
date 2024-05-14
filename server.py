import socket
from _thread import*
import sys
import pickle

server = "192.168.1.112"
port = 8080

s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("waiting for a connection, Server Started")

turn = [1,2]
board = []
for i in range(11):
    board.append([0]*11)

def threaded_client(conn, player):
    conn.send(pickle.dumps(turn[player]))
    reply = []
    while True:
        try:
            data = conn.recv(2048)
            play_pos = pickle.loads(data)
            if play_pos[0]!=-1:
                board[play_pos[0]][play_pos[1]] = play_pos[2]
            if not data:
                print("Disconnected")
                break
            else:
                reply = board

            conn.sendall(pickle.dumps(reply))
        except:
            break

current_player = 0
while True:
    conn, addr = s.accept()
    print("connected to:", addr)

    start_new_thread(threaded_client,(conn,current_player))
    current_player += 1