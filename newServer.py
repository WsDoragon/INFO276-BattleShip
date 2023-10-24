import socket
import json
import time

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
        if len(servidor.jugadoresConectados) == 0:
            player.setTurn(True)
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

        #ver si los 2 jugadores han subido sus barcos
        count = 0
        for jugador in servidor.jugadoresConectados:
            if servidor.jugadoresConectados[jugador].ships == {}:
                break
            else:
                count += 1
                continue

        if count == 2:
            time.sleep(2)
            for jugador in servidor.jugadoresConectados:
                print("enviando turnos a: ", jugador)
                serverJSON["action"] = "t"
                serverJSON["status"] = servidor.jugadoresConectados[jugador].getTurn()
                serverJSONsend = json.dumps(serverJSON)
                UDPServerSocket.sendto(serverJSONsend.encode(), jugador)
        continue

        #Start de partida
    if jsonMessage["action"] == "s" and len(servidor.jugadoresConectados) == 2:
        msgFromServer = "Partida iniciada"
        serverJSON["action"] = "start"
        serverJSON["status"] = 1
        serverJSONsend = json.dumps(serverJSON).encode()
        servidor.jugadoresConectados[address].start = True
        for jugador in servidor.jugadoresConectados:

            if jugador != address and servidor.jugadoresConectados[jugador].start and servidor.jugadoresConectados[address].start:

                servidor.jugadoresConectados[jugador].asignarOponente(servidor.jugadoresConectados[address].address)
                servidor.jugadoresConectados[address].asignarOponente(servidor.jugadoresConectados[jugador].address)
                
                UDPServerSocket.sendto(serverJSONsend, jugador)
                UDPServerSocket.sendto(serverJSONsend, address)
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

        servidor.jugadoresConectados[address].changeTurn()
        servidor.jugadoresConectados[address_opponent].changeTurn()


        if logro:
            print("Le diste a un barco")
            print("atacado por: ", address)
            print(servidor.jugadoresConectados[address_opponent].ships.casillas)
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

        #enviar turnos
        serverJSON["action"] = "t"
        serverJSON["status"] = servidor.jugadoresConectados[address].getTurn()
        serverJSONsend = json.dumps(serverJSON)
        UDPServerSocket.sendto(serverJSONsend.encode(), address)

        serverJSON["status"] = servidor.jugadoresConectados[address_opponent].getTurn()
        serverJSONsend = json.dumps(serverJSON)
        UDPServerSocket.sendto(serverJSONsend.encode(), servidor.jugadoresConectados[address].opponent)
        
        

        """serverJSONsend = json.dumps(serverJSON)
        UDPServerSocket.sendto(serverJSONsend.encode(), address)
        continue"""

    #Handle desconexion de un usuario
    if jsonMessage["action"] == 'd':
        msgFromServer = "Desconexion exitosa"
        #servidor.jugadoresConectados.remove(address)
        #Como eliminar un elemento de un diccionario
        serverJSON = {
            "action"   : "w",
            "status"   : 1
        }
        address_opponent = servidor.jugadoresConectados[address].opponent
        serverJSONsend = json.dumps(serverJSON)
        UDPServerSocket.sendto(serverJSONsend.encode(), address_opponent)

        del servidor.jugadoresConectados[address_opponent]
        print(servidor.jugadoresConectados)
        del servidor.jugadoresConectados[address]
        serverJSON = {
            "action"   : "d",
            "status"   : 1
        }
        serverJSONsend = json.dumps(serverJSON)
        UDPServerSocket.sendto(serverJSONsend.encode(), address)
        
        print(servidor.jugadoresConectados)
        #UDPServerSocket.sendto(msgFromServer.encode(), address)
        continue



    