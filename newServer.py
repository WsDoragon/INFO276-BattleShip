import socket
import json

import clases

servidor = clases.Servidor()

serverJSON = {
    "action"   : "",
    "status"   : 0,
    "position" : [0,0]
}


localIP = "127.0.0.1"
localPort = 20001
bufferSize = 1024
msgFromServer = "Hello UDP Client"
bytesToSend = str.encode(msgFromServer)
# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")
# Listen for incoming datagrams
while(True):

    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]

    jsonMessage = json.loads(message)
    clientMsg = "Message from Client:{}".format(message)
    clientIP = "Client IP Address:{}".format(address)

    print(clientMsg)
    print(clientIP)

    #Handle conexion de un usuario
    if (jsonMessage["action"] == 'conexion' and servidor.jugadoresConectados.count(address) == 0):
        msgFromServer = "Conexion exitosa"
        serverJSON["action"] = "conexion"
        serverJSON["status"] = 1
        servidor.jugadoresConectados.append(address)
        print(servidor.jugadoresConectados)

        serverJSONsend = json.dumps(serverJSON)
        UDPServerSocket.sendto(serverJSONsend.encode(), address)

        continue

    if (jsonMessage["action"] == "start"):
        continue

    #Handle desconexion de un usuario
    if jsonMessage["action"] == 'desconexion':
        msgFromServer = "Desconexion exitosa"
        servidor.jugadoresConectados.remove(address)
        print(servidor.jugadoresConectados)
        UDPServerSocket.sendto(msgFromServer.encode(), address)
        break
        continue

    # Sending a reply to client
    UDPServerSocket.sendto(bytesToSend, address)