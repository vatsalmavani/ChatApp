import socket
import threading
import queue

HOST = 'localhost'
PORT = 9999

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect((HOST, PORT))
server_running = True
q = queue.Queue()

def listen_for_input():
    global server_running
    while server_running:
        message = input('')
        q.put(message)

def send_message():
    global server_running
    while server_running:
        if not q.empty():
            message = q.get()
            try:
                if message == '/exit':
                    clientsocket.send(message.encode('utf-8'))
                    clientsocket.close()
                    server_running = False # since client is exiting, we must end the listen_for_input thread
                    break
                else:
                    clientsocket.send(message.encode('utf-8'))
            except OSError:
                print('connection closed with the server')
                break

def receive_message():
    global server_running
    while server_running:
        try:
            message = clientsocket.recv(4096).decode('utf-8')
            if message == 'SERVER_SHUTDOWN':
                clientsocket.close()
                server_running = False
                break
            else:
                print(message)
        except OSError:
            print('connection closed with the server')
            break

send_thread = threading.Thread(target=send_message)
receive_thread = threading.Thread(target=receive_message)
listen_for_input_thread = threading.Thread(target=listen_for_input)

send_thread.start()
receive_thread.start()
listen_for_input_thread.start()

send_thread.join()
receive_thread.join()
listen_for_input_thread.join()