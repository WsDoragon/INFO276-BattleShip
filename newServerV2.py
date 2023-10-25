import socket
import json
import time

import clasesSala as clases

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

localIP = "localhost"
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
    if (jsonMessage["action"] == 'c' and address not in servidor.jugadoresConectados):
        msgFromServer = "Conexion exitosa"
        serverJSON["action"] = "c"
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
        serverJSON["action"] = "c"
        serverJSON["status"] = 0
        serverJSONsend = json.dumps(serverJSON)
        UDPServerSocket.sendto(serverJSONsend.encode(), address)
        continue

    #Start de partida
    if jsonMessage["action"] == "s":
        msgFromServer = "Partida iniciada"
        serverJSON["action"] = "s"
        serverJSON["status"] = 1
        serverJSONsend = json.dumps(serverJSON).encode()
        servidor.jugadoresConectados[address].start = True

        if address not in servidor.jugadoresEsperando and jsonMessage["bot"] == 0:
            print("entro jugador")
            if(len(servidor.jugadoresEsperando) == 0):
                servidor.jugadoresConectados[address].setTurn(True)
            servidor.addJugadorEspera(servidor.jugadoresConectados[address])
            if len(servidor.jugadoresEsperando) == 2:

                for jugador in servidor.jugadoresEsperando:

                    if jugador != address and servidor.jugadoresEsperando[jugador].start and servidor.jugadoresEsperando[address].start:

                        servidor.jugadoresEsperando[jugador].asignarOponente(servidor.jugadoresEsperando[address].address)
                        servidor.jugadoresEsperando[address].asignarOponente(servidor.jugadoresEsperando[jugador].address)

                        servidor.addJugadorPartida(servidor.jugadoresEsperando[jugador])
                        servidor.addJugadorPartida(servidor.jugadoresEsperando[address])

                        servidor.jugadoresEsperando = {}
                        
                        UDPServerSocket.sendto(serverJSONsend, jugador)
                        UDPServerSocket.sendto(serverJSONsend, address)
                        print("sending to: ",jugador)

        
        elif (address not in servidor.jugadoresBot and jsonMessage["bot"] == 1):
            print("entro jugador vs bot")
            if(len(servidor.jugadoresBot) == 0):
                servidor.jugadoresConectados[address].setTurn(True)
            servidor.addJugadorBot(servidor.jugadoresConectados[address])

            print(servidor.jugadoresBot, "bot", len(servidor.jugadoresBot))

            if len(servidor.jugadoresBot) == 2:

                for jugador in servidor.jugadoresBot:

                    if jugador != address and servidor.jugadoresBot[jugador].start and servidor.jugadoresBot[address].start:

                        servidor.jugadoresBot[jugador].asignarOponente(servidor.jugadoresBot[address].address)
                        servidor.jugadoresBot[address].asignarOponente(servidor.jugadoresBot[jugador].address)

                        servidor.addJugadorPartida(servidor.jugadoresBot[jugador])
                        servidor.addJugadorPartida(servidor.jugadoresBot[address])

                        servidor.jugadoresBot = {}
                        
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

    #Build de tablero
    if jsonMessage["action"] == 'b':
        msgFromServer = "Tablero construido"
        serverJSON["action"] = "b"
        serverJSON["status"] = 1
        naves = jsonMessage["ships"]
        mis_naves = clases.Barcos(naves)
        servidor.jugadoresPartida[address].añadirBarco(mis_naves)
        print(servidor.jugadoresPartida[address].obtenerBarcos())
        #for nave in shipTypes:
        #    print(naves[nave])
            #sendShips = clases.Barcos(naves)

        serverJSONsend = json.dumps(serverJSON)
        UDPServerSocket.sendto(serverJSONsend.encode(), address)

        #ver si los 2 jugadores han subido sus barcos
        count = 0
        address_opponent = servidor.jugadoresPartida[address].opponent
        if servidor.jugadoresPartida[address].ships == {} or servidor.jugadoresPartida[address_opponent].ships == {}:
            continue
        else:
            serverJSON["action"] = "t"
            serverJSON["status"] = servidor.jugadoresPartida[address].getTurn()
            print("enviando turnos a: ", address , "turno", servidor.jugadoresPartida[address].getTurn())
            serverJSONsend = json.dumps(serverJSON)
            UDPServerSocket.sendto(serverJSONsend.encode(), address)

            serverJSON["status"] = servidor.jugadoresPartida[address_opponent].getTurn()
            print("enviando turnos a: ", address_opponent , "turno", servidor.jugadoresPartida[address_opponent].getTurn())
            serverJSONsend = json.dumps(serverJSON)
            UDPServerSocket.sendto(serverJSONsend.encode(), address_opponent)

        continue


    

        #Ataque de un usuario
    if jsonMessage["action"] == 'a':
        msgFromServer = "Ataque realizado"
        serverJSON["action"] = "a"
        serverJSON["status"] = 1
        serverJSON["position"] = jsonMessage["position"]

        address_opponent = servidor.jugadoresPartida[address].opponent
        logro = servidor.jugadoresPartida[address_opponent].ships.recibirAtaque(jsonMessage["position"])

        servidor.jugadoresPartida[address].changeTurn()
        servidor.jugadoresPartida[address_opponent].changeTurn()


        if logro:
            print("Le diste a un barco")
            print("atacado por: ", address)
            print(servidor.jugadoresPartida[address_opponent].ships.casillas)
            if servidor.jugadoresPartida[address_opponent].ships.casillas == []:
                print("Ganaste")
                serverJSON["action"] = "l" #lost
                serverJSON["status"] = 0
                serverJSONsend = json.dumps(serverJSON)
                UDPServerSocket.sendto(serverJSONsend.encode(), address)
                #Falta cambiar que le llegue un 0 al otro jugador cuando pierde
                serverJSON["action"] = "l"
                serverJSON["status"] = 1
                serverJSONsend = json.dumps(serverJSON)
                UDPServerSocket.sendto(serverJSONsend.encode(), servidor.jugadoresPartida[address].opponent)
                
                #desconexion de jugadores y eliminacion de partida
                del servidor.jugadoresConectados[address_opponent]
                del servidor.jugadoresPartida[address_opponent]
                print(servidor.jugadoresConectados)
                del servidor.jugadoresConectados[address]
                del servidor.jugadoresPartida[address]

                break
            else:
                serverJSON["action"] = "a"
                serverJSON["status"] = 1
                serverJSONsend = json.dumps(serverJSON)
                UDPServerSocket.sendto(serverJSONsend.encode(), address)
                UDPServerSocket.sendto(serverJSONsend.encode(), servidor.jugadoresPartida[address].opponent)



                
        else:
            print("Fallaste")
            serverJSON["action"] = "a"
            serverJSON["status"] = 0
            serverJSONsend = json.dumps(serverJSON)
            UDPServerSocket.sendto(serverJSONsend.encode(), address)
            UDPServerSocket.sendto(serverJSONsend.encode(), servidor.jugadoresPartida[address].opponent)

        #enviar turnos
        serverJSON["action"] = "t"
        serverJSON["status"] = servidor.jugadoresPartida[address].getTurn()
        serverJSONsend = json.dumps(serverJSON)
        UDPServerSocket.sendto(serverJSONsend.encode(), address)

        serverJSON["status"] = servidor.jugadoresPartida[address_opponent].getTurn()
        serverJSONsend = json.dumps(serverJSON)
        UDPServerSocket.sendto(serverJSONsend.encode(), servidor.jugadoresPartida[address].opponent)
        
        

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
        address_opponent = servidor.jugadoresPartida[address].opponent
        serverJSONsend = json.dumps(serverJSON)
        UDPServerSocket.sendto(serverJSONsend.encode(), address_opponent)

        del servidor.jugadoresConectados[address_opponent]
        del servidor.jugadoresPartida[address_opponent]
        print(servidor.jugadoresConectados)
        del servidor.jugadoresConectados[address]
        del servidor.jugadoresPartida[address]
        serverJSON = {
            "action"   : "d",
            "status"   : 1
        }
        serverJSONsend = json.dumps(serverJSON)
        UDPServerSocket.sendto(serverJSONsend.encode(), address)
        
        print(servidor.jugadoresConectados)
        #UDPServerSocket.sendto(msgFromServer.encode(), address)
        continue



    