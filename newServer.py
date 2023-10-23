import socket
import json

import clases

servidor = clases.Servidor()

serverJSON = {
    "action"   : "",
    "status"   : 0,
    "position" : [0,0]
}

acciones = {
    "c" : "connect",
    "s" : "start",
    "a" : "attack",
    "d" : "desconectar",
    "b" : "build",
    "d" : "disconnect",
    "l" : "lost"

}

shipTypes = ["p","b","s"]

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
    if (jsonMessage["action"] == 'c' and address not in servidor.jugadoresConectados and len(servidor.jugadoresConectados) < 2):
        msgFromServer = "Conexion exitosa"
        serverJSON["action"] = "conexion"
        serverJSON["status"] = 1
        player = clases.Jugador(address)
        servidor.jugadoresConectados[address] = player
        #servidor.jugadoresConectados.append(address)
        print(servidor.jugadoresConectados)

        serverJSONsend = json.dumps(serverJSON)
        UDPServerSocket.sendto(serverJSONsend.encode(), address)

        continue

    elif(jsonMessage["action"] == 'c' and address not in servidor.jugadoresConectados  and len(servidor.jugadoresConectados) >= 2):
        msgFromServer = "Conexion fallida"
        serverJSON["action"] = "conexion"
        serverJSON["status"] = 0
        serverJSONsend = json.dumps(serverJSON)
        UDPServerSocket.sendto(serverJSONsend.encode(), address)
        continue

    #Build de tablero
    if jsonMessage["action"] == 'b':
        msgFromServer = "Tablero construido"
        serverJSON["action"] = "build"
        serverJSON["status"] = 1
        naves = jsonMessage["ships"]
        mis_naves = clases.Barcos(naves)
        servidor.jugadoresConectados[address].añadirBarco(mis_naves)
        print(servidor.jugadoresConectados[address].obtenerBarcos())
        #for nave in shipTypes:
        #    print(naves[nave])
            #sendShips = clases.Barcos(naves)
        serverJSONsend = json.dumps(serverJSON)
        UDPServerSocket.sendto(serverJSONsend.encode(), address)

        
        continue

        #Start de partida
    if jsonMessage["action"] == "s" and len(servidor.jugadoresConectados) == 2:
        msgFromServer = "Partida iniciada"
        serverJSON["action"] = "start"
        serverJSON["status"] = 1
        serverJSONsend = json.dumps(serverJSON).encode()
        for jugador in servidor.jugadoresConectados:

            if jugador != address:

                servidor.jugadoresConectados[jugador].asignarOponente(servidor.jugadoresConectados[address].address)
                servidor.jugadoresConectados[address].asignarOponente(servidor.jugadoresConectados[jugador].address)
                
            UDPServerSocket.sendto(serverJSONsend, jugador)
            print("sending to: ",jugador)
           #print (servidor.jugadoresConectados[jugador].opponent)

    elif(jsonMessage["action"] == "s" and len(servidor.jugadoresConectados) < 2):
        msgFromServer = "Partida no iniciada"
        serverJSON["action"] = "start"
        serverJSON["status"] = 0
        serverJSONsend = json.dumps(serverJSON)


        UDPServerSocket.sendto(serverJSONsend.encode(), address)
        continue

        #Ataque de un usuario
    if jsonMessage["action"] == 'a':
        msgFromServer = "Ataque realizado"
        serverJSON["action"] = "attack"
        serverJSON["status"] = 1
        serverJSON["position"] = jsonMessage["position"]

        address_opponent = servidor.jugadoresConectados[address].opponent
        logro = servidor.jugadoresConectados[address_opponent].ships.recibirAtaque(jsonMessage["position"])

        if logro:
            print("Le diste a un barco")
            if servidor.jugadoresConectados[address_opponent].ships.casillas == []:
                print("Ganaste")
                serverJSON["action"] = "l" #lost
                serverJSON["status"] = 0
                serverJSONsend = json.dumps(serverJSON)
                UDPServerSocket.sendto(serverJSONsend.encode(), address)
                #Falta cambiar que le llegue un 0 al otro jugador cuando pierde
                serverJSON["action"] = "l"
                serverJSON["status"] = 1
                serverJSONsend = json.dumps(serverJSON)
                UDPServerSocket.sendto(serverJSONsend.encode(), servidor.jugadoresConectados[address].opponent)
                break
            else:
                serverJSON["action"] = "a"
                serverJSON["status"] = 1
                serverJSONsend = json.dumps(serverJSON)
                UDPServerSocket.sendto(serverJSONsend.encode(), address)
                UDPServerSocket.sendto(serverJSONsend.encode(), servidor.jugadoresConectados[address].opponent)
                
        else:
            print("Fallaste")
            serverJSON["action"] = "a"
            serverJSON["status"] = 0
            serverJSONsend = json.dumps(serverJSON)
            UDPServerSocket.sendto(serverJSONsend.encode(), address)
            UDPServerSocket.sendto(serverJSONsend.encode(), servidor.jugadoresConectados[address].opponent)
        
        

        """serverJSONsend = json.dumps(serverJSON)
        UDPServerSocket.sendto(serverJSONsend.encode(), address)
        continue"""

    #Handle desconexion de un usuario
    if jsonMessage["action"] == 'd':
        msgFromServer = "Desconexion exitosa"
        servidor.jugadoresConectados.remove(address)
        #Como eliminar un elemento de un diccionario
        del servidor.jugadoresConectados[address]
        
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
    