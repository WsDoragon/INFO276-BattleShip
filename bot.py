import socket
import json
import board as bd
import random as rand


class bot():

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.sock.connect((host, port))
        #self.sock.send("conexion".encode())
        self.botShips = {}
        self.attackList = []

    def connect(self):
        jsonBot = {
            "action": "c"
        }
        self.sock.send(json.dumps(jsonBot).encode())
        data = self.sock.recv(1024)
        receivedJSON = json.loads(data.decode())
        #print("bot: ",receivedJSON)

    def build(self):
        board =  bd.build_board(5)
        ships = [["p",1], ["b",2], ["s",3]]
        self.botShips = {}
        for ship in ships:
            #print("|Tablero actual|")
            #print("Tamano del barco: ", ship[1])
            #board.print_board(board)
            direction = rand.choice(["h", "v"])
            if direction == "h":
                x = rand.randint(0,4)
                y = rand.randint(0,4-ship[1])
                while bd.check_ship(board, x, y, ship[1], direction):
                    x = rand.randint(0,4)
                    y = rand.randint(0,4-ship[1])
            else:
                x = rand.randint(0,4-ship[1])
                y = rand.randint(0,4)
                while bd.check_ship(board, x, y, ship[1], direction):
                    x = rand.randint(0,4-ship[1])
                    y = rand.randint(0,4)
            self.botShips[ship[0]] = [x,y,direction == "h"]
            bd.put_ship(board, ship[1], x, y, direction)
    
    def start(self):
        jsonBot = {
            "action": "s",
            "bot": 1
        }
        self.sock.send(json.dumps(jsonBot).encode())
        data = self.sock.recv(1024)
        receivedJSON = json.loads(data.decode())
        #print("bot: ",receivedJSON)

    def sendBuild(self):
        jsonBot = {
            "action": "b",
            "ships": {'p': [0, 0, True], 'b': [0, 3, True], 's': [1, 2, True]}
        }
        self.sock.send(json.dumps(jsonBot).encode())
        #print("bot: Enviado ships" , self.botShips)
        data = self.sock.recv(1024)
        #print("bot: recibido ships")
        receivedJSON = json.loads(data.decode())
        self.gaming = True
        #print("bot: ",receivedJSON)

    def attack(self):
        x = rand.randint(0,4)
        y = rand.randint(0,4)
        while [x,y] in self.attackList:
            x = rand.randint(0,4)
            y = rand.randint(0,4)
        self.attackList.append([x,y])
        return [x,y]
    
    def playTime(self):
        while self.gaming:
            #recibir turno
            data = self.sock.recv(1024)
            receivedJSON = json.loads(data.decode())
            print("bot: ",receivedJSON)

            if(receivedJSON["action"] == "t" and receivedJSON["status"] == 1):
                cordenadas = self.attack()
                jsonBot = {
                    "action": "a",
                    "position": cordenadas
                }

                self.sock.send(json.dumps(jsonBot).encode())

                

