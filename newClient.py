import socket
import json

jsonUser = {
    "action": "",
}


def client_terminal():
    # create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # define the server address and port
    server_address = ('localhost', 20001)

    # send a message to the server
    JsonUSer = {
        "action": "c"
    }
    message = json.dumps(JsonUSer).encode()
    sock.sendto(message, server_address)

    # receive a response from the server
    data, address = sock.recvfrom(4096)
    receivedJSON = json.loads(data)
    print(receivedJSON)

    # send a message to the server
    startEntry = input("Ingrese comando 'start - [N°]' (1: bot - 0:User): ").split("-")
    JsonUSer = {
        "action": "s",
        #En caso de tener 1 en el comando, se conecta con el bot en otro caso se pone un 0
        "bot": startEntry[1]
    }
    message = json.dumps(JsonUSer).encode()
    sock.sendto(message, server_address)

    # receive a response from the server
    data, address = sock.recvfrom(4096)
    receivedJSON = json.loads(data)
    print(receivedJSON)
    
    #print(f'Received "{data.decode()}" from {address}')

    # close the socket
    sock.close()
