import socket
import threading

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_host = '192.168.48.205'
server_port = 8080

server_socket.bind((server_host, server_port))
server_socket.listen(2)

print(f"Server is listening on {server_host}:{server_port}")

clients = []
# Số lượng kết nối
client_count = 0
is_clients_connected = False  # Biến cờ để kiểm tra xem có client nào đang kết nối hay không

# Hàm gửi dữ liệu đến tất cả các client
def send_to_all_clients(message, sender):
    for client in clients:
        if client != sender:
            try:
                client.sendall(message.encode())
            except Exception as e:
                print(f"Error sending data to client: {e}")
                remove_client(client)
                client.close()

# Hàm xử lý kết nối từ mỗi client
def handle_client(client_socket, client_address):
    global is_clients_connected  # Sử dụng biến cờ toàn cục
    global client_count
    print(f"Connected to {client_address}")
    client_count += 1
    print(f"Client_connect: {client_count}")
    is_clients_connected = True  # Đặt cờ thành True khi có một client kết nối

    while True:
        try:
            data = client_socket.recv(2048).decode()
            if not data:
                print(f"Disconnected from {client_address}")
                break
            send_to_all_clients(data, client_socket)
            send_to_all_clients(f"SERVER:{client_count}", client_socket)
        except Exception as e:
            print(f"Error handling data from {client_address}: {e}")
            break

    remove_client(client_socket)
    client_socket.close()

def remove_client(client):
    global client_count
    clients.remove(client)
    client_count -= 1
    print(f"Client_connect: {client_count}")
    send_to_all_clients(f"SERVER:{client_count}", client_socket)
    if not clients:  # Kiểm tra nếu không còn client nào kết nối
        is_clients_connected = False  # Đặt cờ thành False

while True:
    try:
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)

        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()
    except Exception as e:
        print(f"Error accepting connection from client: {e}")

server_socket.close()
