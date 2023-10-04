import socket
import json
import threading

def inicial():
    msgFromClient = "conexio"
    bytesToSend = str.encode(msgFromClient)
    serverAddressPort = ("127.0.0.1", 21000)
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


#------------------------------------------------
def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024).decode()
            if not data:
                continue  # Ignorar datos vacíos
            print(data)
            receivedJSON = json.loads(data)
            print("Received from server:", receivedJSON)

            if receivedJSON.get("action") == "desconectar":
                break
        except json.decoder.JSONDecodeError as e:
            print("Error al decodificar JSON:", str(e))
        except Exception as e:
            print("Error en la recepción de mensajes:", str(e))
            # Manejar otras excepciones de manera adecuada, por ejemplo, reconectar o salir del hilo.

def client_terminal():
    host = "localhost"
    port = 21000

    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    sock.connect((host, port))
    print(sock)

    # Iniciar un hilo para recibir mensajes en segundo plano
    receive_thread = threading.Thread(target=receive_messages, args=(sock,))
    receive_thread.start()
#UPnP - OWASP - arachni
    while True:
        msg = input("-> ")
        msg = msg.split(" - ")
        myJSON = {
            "action": msg[0],
            "bot": msg[1]
        }
        myJSON = json.dumps(myJSON)
        sock.send(myJSON.encode())

        if msg == "desconectar":
            break


def client_terminalF():
    host = "localhost"
    port = 21000

    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    sock.connect((host, port))
    print(sock)
    while True:
        msg = input("-> ")
        myJSON = {
            "action" : msg
        }
        myJSON = json.dumps(myJSON)
        sock.send(myJSON.encode())
        data = sock.recv(1024).decode()
        print(data)
        receivedJSON = json.loads(data)
        print("Received from server: " , receivedJSON)

        if(receivedJSON["action"] == "desconectar"):
            break

        


if __name__ == '__main__':
    client_terminal()