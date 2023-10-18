import socket
import json

jsonUser = {
    "action": "",
}


def client_terminal():
    # create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    retrys = 0

    # define the server address and port
    server_address = ('localhost', 20001)

    # send a message to the server
    JsonUSer = {
        "action": "c"
    }
    #Paso de conexion
    continues = True
    while (continues == True):
        message = json.dumps(JsonUSer).encode()
        sock.sendto(message, server_address)

        # receive a response from the server
        data, address = sock.recv(1024)
        receivedJSON = json.loads(data.decode())
        print(receivedJSON)

        

        if(receivedJSON["status"] == 0):
            retries += 1
            print("Conexion fallida reintentando...")
            if(retries == 3):
                print("Conexion fallida\nCerrando Programa...")
                sock.close()
                exit()

        elif(receivedJSON["status"] == 1):
            print("Conexion exitosa")
            continues = False

    

    # send a message to the server
    startEntry = input("Ingrese comando 'start - [N°]' (1: bot - 0:User): ").split("-")
    JsonUSer = {
        "action": "s",
        #En caso de tener 1 en el comando, se conecta con el bot en otro caso se pone un 0
        "bot": startEntry[1]
    }

    message = json.dumps(JsonUSer).encode()
    sock.sendto(message, server_address)

    # Configurar el timeout en 1 segundo
    sock.settimeout(10)

    # Enviar un mensaje al servidor
    try:
        sent = sock.sendto(message, server_address)

        # Esperar la respuesta del servidor
        data, server = sock.recv(1024)
        print('Received:', data.decode())
    except socket.timeout:
        # Si se produce un timeout, reintentar el envío del mensaje
        print('Timeout, reintentando...')
        sent = sock.sendto(message, server_address)

    
    #Envio barcos
    JsonUSer = {
        "action": "b",
        "ships": {'p': [0, 0, True], 'b': [0, 3, True], 's': [1, 2, True]}
    }

    message = json.dumps(JsonUSer).encode()
    sock.sendto(message, server_address)

    # receive a response from the server
    data, address = sock.recvfrom(1024)
    receivedJSON = json.loads(data.decode())
    print("Datos validados de build\n",receivedJSON, "\n")

    gaming = True
    while (gaming):
        #Recepcion turno
        data, address = sock.recvfrom(1024)
        receivedJSONTurn = json.loads(data.decode())
        print(receivedJSONTurn)
        if(receivedJSONTurn["status"] == 1):
            #Envio ataque
            attackEntry = input("Ingrese comando 'attack - [x,y]': ").split("-")
            JsonUSer = {
                "action": "a",
                "position": [int(attackEntry[1]), int(attackEntry[2])]
            }

            message = json.dumps(JsonUSer).encode()
            sock.sendto(message, server_address)

            #Recepcion de ataque
            data, address = sock.recvfrom(1024)
            receivedJSON = json.loads(data.decode())
            print(receivedJSON)

            if(receivedJSON["action"] == "l" and receivedJSON["status"] == 1):
                print("Perdiste")
                gaming = False
                continue
            elif(receivedJSON["action"] == "l" and receivedJSON["status"] == 0):
                print("Ganaste")
                gaming = False
                continue

            elif(receivedJSON["action"] == "a" and receivedJSON["status"] == 1):
                print("Ataque exitoso")
                continue
            else:
                print("Ataque fallido")
                continue

        else:
            print("Esperando turno...")
            #recibir confirmacion ataque enemigo
            data, address = sock.recvfrom(1024)
            receivedJSON = json.loads(data.decode())
            print(receivedJSON)
            ##logica de ataques enemigos
            #
            continue




    



    # receive a response from the server
    data, address = sock.recvfrom(4096)
    receivedJSON = json.loads(data)
    print(receivedJSON)
    
    #print(f'Received "{data.decode()}" from {address}')

    # close the socket
    sock.close()
