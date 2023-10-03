import socket
import json

def inicial():
    msgFromClient = "conexio"
    bytesToSend = str.encode(msgFromClient)
    serverAddressPort = ("127.0.0.1", 20001)
    bufferSize = 1024
    # Create a UDP socket at client side
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    # Send to server using created UDP socket
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    msg = "Message from Server {}".format(msgFromServer[0])
    print(msg)

def client_program():
    #host = socket.gethostname()  # as both code is running on same pc
    host = "127.0.0.1"
    port = 20001  # socket server port number

    client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)  # instantiate
    client_socket.connect((host, port))  # connect to the server

    message = input(" -> ")  # take input

    while message.lower().strip() != 'bye':
        client_socket.send(message.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response

        print('Received from server: ' + data)  # show in terminal

        message = input(" -> ")  # again take input

    client_socket.close()  # close the connection

def client_terminal():
    host = "localhost"
    port = 20001

    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    sock.connect((host, port))

    while True:
        msg = input("-> ")
        myJSON = {
            "action" : msg
        }
        myJSON = json.dumps(myJSON)
        sock.send(myJSON.encode())
        data = sock.recv(1024).decode()

        receivedJSON = json.loads(data)
        print("Received from server: " + receivedJSON["action"])


if __name__ == '__main__':
    client_terminal()