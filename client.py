import socket
import threading

HOST = 'localhost'
PORT = 9999

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect((HOST, PORT))


def send_message():
    while True:
        message = input('')
        try:
            if message == '/exit':
                clientsocket.send(message.encode('utf-8'))
                clientsocket.close()
                break
            else:
                clientsocket.send(message.encode('utf-8'))
        except OSError:
            print('connection closed with the server')
            break

def receive_message():
    while True:
        try:
            message = clientsocket.recv(4096).decode('utf-8')
            if message == 'SERVER_SHUTDOWN':
                clientsocket.close()
                break
            else:
                print(message)
        except OSError:
            print('connection closed with the server')
            break

send_thread = threading.Thread(target=send_message)
receive_thread = threading.Thread(target=receive_message)

send_thread.start()
receive_thread.start()

send_thread.join()
receive_thread.join()