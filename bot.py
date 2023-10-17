import socket
import board
import random as rand


class bot():

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.sock.connect((host, port))
        self.sock.send("conexion".encode())

    def build(self):
        board =  board.build_game(5)
        ships = [["p",1], ["b",2], ["s",3]]
        self.botShips = {}
        for ship in ships:
            print("|Tablero actual|")
            print("Tamano del barco: ", ship[1])
            #board.print_board(board)
            direction = rand.choice(["h", "v"])
            if direction == "h":
                x = rand.randint(0,4)
                y = rand.randint(0,4-ship[1])
            else:
                x = rand.randint(0,4-ship[1])
                y = rand.randint(0,4)
            self.botShips[ship[0]] = [x,y,direction]
            board.put_ship(board, ship[1], x, y, direction)