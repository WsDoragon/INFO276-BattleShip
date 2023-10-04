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
localPort = 21000
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
    if (jsonMessage["action"] == 'conexion' and servidor.jugadoresConectados.count(address) == 0 and len(servidor.jugadoresConectados) < 2):
        msgFromServer = "Conexion exitosa"
        serverJSON["action"] = "conexion"
        serverJSON["status"] = 1
        servidor.jugadoresConectados.append(address)
        print(servidor.jugadoresConectados)

        serverJSONsend = json.dumps(serverJSON)
        UDPServerSocket.sendto(serverJSONsend.encode(), address)

        continue

    elif(jsonMessage["action"] == 'conexion' and servidor.jugadoresConectados.count(address) > 0 and len(servidor.jugadoresConectados) >= 2):
        msgFromServer = "Conexion fallida"
        serverJSON["action"] = "conexion"
        serverJSON["status"] = 0
        serverJSONsend = json.dumps(serverJSON)
        UDPServerSocket.sendto(serverJSONsend.encode(), address)
        continue

    if jsonMessage["action"] == "start" and len(servidor.jugadoresConectados) == 2:
        msgFromServer = "Partida iniciada"
        serverJSON["action"] = "start"
        serverJSON["status"] = 1
        serverJSONsend = json.dumps(serverJSON).encode()
        for jugador in servidor.jugadoresConectados:
            #print(serverJSON)
            UDPServerSocket.sendto(serverJSONsend, jugador)
            print("sending to: ",jugador)

    elif(jsonMessage["action"] == "start" and len(servidor.jugadoresConectados) < 2):
        msgFromServer = "Partida no iniciada"
        serverJSON["action"] = "start"
        serverJSON["status"] = 0
        serverJSONsend = json.dumps(serverJSON)


        UDPServerSocket.sendto(serverJSONsend.encode(), address)
        continue

    #Handle desconexion de un usuario
    if jsonMessage["action"] == 'desconexion':
        msgFromServer = "Desconexion exitosa"
        servidor.jugadoresConectados.remove(address)
        print(servidor.jugadoresConectados)
        UDPServerSocket.sendto(msgFromServer.encode(), address)
        break
        continue

    if jsonMessage["action"] == 'a':
        msgFromServer = "Desconexion exitosa"
        servidor.jugadoresConectados.remove(address)
        print(servidor.jugadoresConectados)
        serverJSON["action"] = "desconectar"
        serverJSON["status"] = 1
        serverJSONsend = json.dumps(serverJSON)

        UDPServerSocket.sendto(serverJSONsend.encode(), address)
        break
        continue
    