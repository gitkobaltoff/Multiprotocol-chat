import threading
import socket
HOST = '127.0.0.1'
PORT = 1234

# TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    """
        Sends an already encoded message to all connected clients, except the source of the message.
        Args:
            message (str): The message to broadcast.
    """
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{nicknames[clients.index(client)]} says {message}")
            broadcast(message)
        except:
            # error handling
            index = clients.index(client)
            # remove the client and close the connection
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f"{nickname} left the chat".encode('utf-8'))
            nicknames.remove(nickname)
            # end the thread
            break

def reveive():
    while True:
        # accept the connection
        client, address = server.accept()
        print(f"Address: {str(address)}")

        # send the keyword NICK in order to request a nickname
        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')

        # append the new client and nickname
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname: {nickname}")
        broadcast(f"{nickname} joined the chat\n".encode('utf-8'))
        # message sent to the particular client
        client.send('Connected to the server'.encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print('Server is listening...')
reveive()