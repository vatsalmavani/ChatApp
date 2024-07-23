import socket
import threading

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST, PORT = 'localhost', 9999
serversocket.bind((HOST, PORT))
serversocket.listen(10) # accept max of 10 connections

server_running = True
client_threads = [] # shared list among threads
client_threads_lock = threading.Lock()

def handle_client(clientsocket:socket.socket):
    '''get message from the client
    if message == "/exit": remove_client(), else, broadcast_message()'''

    global server_running

    def receive_message():
        try:
            message = clientsocket.recv(4096).decode('utf-8')
            return message
        except:
            return 'ConnectionError' # connection was broken

    def remove_client():
        with client_threads_lock:
            # since 'client_threads' array can be modified by other threads,
            # lock is required to prevent undefined behavisr
            for ct in client_threads:
                if ct.clientsocket == clientsocket:
                    client_threads.remove(ct)
                    break
            clientsocket.close()

    def broadcast_message(message):
        with client_threads_lock:
            for ct in client_threads:
                if ct.clientsocket != clientsocket:
                    try:
                        ct.clientsocket.sendall(message.encode('utf-8'))
                    except:
                        continue


    while server_running:
        message = receive_message()
        if message == '/exit' or message == 'ConnectionError':
            remove_client()
            break
        else:
            broadcast_message(message)

def listen_for_exit():
    global server_running

    while server_running:
        if input('') == 'exit()':
            with client_threads_lock:
                for ct in client_threads:
                    try:
                        ct.clientsocket.send('SERVER_SHUTDOWN'.encode('utf-8'))
                        ct.clientsocket.close()
                    except:
                        continue
                client_threads.clear()
            serversocket.close()
            server_running = False          

exit_thread = threading.Thread(target=listen_for_exit)
exit_thread.start()

serversocket.settimeout(1) # timeout for serversocket.accept() - to repeatedly check 'server_running'

while server_running:
    try:
        clientsocket, address = serversocket.accept()
        ct = threading.Thread(target=handle_client, args=(clientsocket,))
        ct.clientsocket = clientsocket # add a 'clientsocket' attribute to the client thread object
        with client_threads_lock: # since remove_client function may be removing a client thread concurrently
            client_threads.append(ct)
        ct.start()
    except socket.timeout:
        continue
    except: # server shutdown
        break

with client_threads_lock:
    for ct in client_threads:
        ct.join()
exit_thread.join()