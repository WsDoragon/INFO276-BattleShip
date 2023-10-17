import socket
import json
import threading
import time

from board import build_game
# ------------------------------------------------
gameInit_lock = threading.Lock()
gameInit = False

def receive_messages(sock):
    global gameInit
    with gameInit_lock:
        gameInit = False
    while True:
        try:
            data = sock.recv(1024).decode()
            if not data:
                continue  # Ignorar datos vacíos
            print(data)
            receivedJSON = json.loads(data)
            print("Received from server:", receivedJSON)

            if receivedJSON['action'] == 'start' and receivedJSON["status"] == 1:
                print("Partida iniciada")
                with gameInit_lock:
                    gameInit = True

            if receivedJSON.get("action") == "desconectar":
                break
        except json.decoder.JSONDecodeError as e:
            print("Error al decodificar JSON:", str(e))
        except Exception as e:
            print("Error en la recepción de mensajes:", str(e))




def client_terminal():
    global gameInit
    host = "localhost"
    port = 21000

    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    sock.connect((host, port))
    print(sock)
    # Iniciar un hilo para recibir mensajes en segundo plano
    receive_thread = threading.Thread(target=receive_messages, args=(sock,))
    receive_thread.start()

    #Creacion tablero usuario
    #user_ships, userBoard = build_game(5)
    #print(user_ships)

    input("Presione ENTER para conectarse al servidor...")
    myJSON = {
        "action": "conexion"
    }
    myJSON = json.dumps(myJSON)
    sock.send(myJSON.encode())

    while True:
        
            while not gameInit:
                msg = input("-> ")
                msg = msg.split(" - ")

                if msg[0] == "build":
                    myJSON = {
                        "action": msg[0],
                        "ships": {'p': [0, 0, True], 'b': [0, 3, True], 's': [1, 2, True]}
                    }

                elif msg[0] == "start" and len(msg) == 2:
                    myJSON = {
                        "action": msg[0],
                        "bot": msg[1]
                    }
                    if msg[1] == "1":
                        sockBot = socket.socket(
                            family=socket.AF_INET, type=socket.SOCK_DGRAM)
                        sockBot.connect((host, port))
                        botJSON = {
                            "action": "conexion"
                        }
                        sockBot.send(json.dumps(botJSON).encode())
                else:
                    myJSON = {
                        "action": msg[0],
                    }

                if msg[0] == "a":
                    myJSON = json.dumps(myJSON)
                    sock.send(myJSON.encode())
                    break

                myJSON = json.dumps(myJSON)
                sock.send(myJSON.encode())

                if msg[0] == "desconectar":
                    break
                delay = 0.5
                time.sleep(delay)
            print("sali?", gameInit)
            
            while gameInit:
                print("Esperando turno...")
                msg = input("ataque(x,y) -> ")
                if msg == "exit":
                    exit()
                while len(msg) != 3:
                    msg = input("ataque(x,y) -> ")
                msgSplit = msg.split(",")
                myJSON = {
                    "action": "attack",
                    "position": [int(msgSplit[0]), int(msgSplit[1])]
                }
                myJSON = json.dumps(myJSON)
                sock.send(myJSON.encode())
                #data = sock.recv(1024).decode()
                #receivedJSON = json.loads(data)
                #print("Received from server: ", receivedJSON)

                #if receivedJSON["action"] == "desconectar":
                #    break

if __name__ == '__main__':
    client_terminal()
