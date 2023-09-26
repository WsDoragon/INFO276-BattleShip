import socket
import clases

servidor = clases.Servidor()


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
    clientMsg = "Message from Client:{}".format(message)
    clientIP = "Client IP Address:{}".format(address)

    #Handle conexion de un usuario
    if message == b'conexion':
        msgFromServer = "Conexion exitosa"
        servidor.jugadoresConectados.append(address[0])
        print(servidor.jugadoresConectados)
        UDPServerSocket.sendto(msgFromServer.encode(), address)

        continue

    print(clientMsg)
    print(clientIP)

    #Handle desconexion de un usuario
    if message == b'desconexion':
        msgFromServer = "Desconexion exitosa"
        servidor.jugadoresConectados.remove(address[0])
        print(servidor.jugadoresConectados)
        UDPServerSocket.sendto(msgFromServer.encode(), address)

        continue

    # Sending a reply to client
    UDPServerSocket.sendto(bytesToSend, address)