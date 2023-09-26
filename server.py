import socket
import random
import threading

class BattleshipGame:
    def __init__(self, player1_address, player2_address):
        self.player1_address = player1_address
        self.player2_address = player2_address
        self.board1 = self.create_board()
        self.board2 = self.create_board()
        self.ships1 = [5, 4, 4, 3, 3, 3, 2, 2, 2, 2]
        self.ships2 = [5, 4, 4, 3, 3, 3, 2, 2, 2, 2]
        self.turn = 1
        self.game_over = False

    def create_board(self):
        return [[0 for x in range(10)] for y in range(10)]

    def place_ships(self, board, ships):
        for ship in ships:
            while True:
                x = random.randint(0, 9)
                y = random.randint(0, 9)
                orientation = random.randint(0, 1)
                if orientation == 0 and x + ship <= 10:
                    valid = True
                    for i in range(ship):
                        if board[x+i][y] != 0:
                            valid = False
                            break
                    if valid:
                        for i in range(ship):
                            board[x+i][y] = ship
                        break
                elif orientation == 1 and y + ship <= 10:
                    valid = True
                    for i in range(ship):
                        if board[x][y+i] != 0:
                            valid = False
                            break
                    if valid:
                        for i in range(ship):
                            board[x][y+i] = ship
                        break

    def get_board(self, player):
        if player == 1:
            return self.board1
        else:
            return self.board2

    def get_ships(self, player):
        if player == 1:
            return self.ships1
        else:
            return self.ships2

    def get_opponent_address(self, player):
        if player == 1:
            return self.player2_address
        else:
            return self.player1_address

    def get_player_address(self, player):
        if player == 1:
            return self.player1_address
        else:
            return self.player2_address

    def get_player_number(self, address):
        if address == self.player1_address:
            return 1
        else:
            return 2

    def get_message(self, message):
        x, y = map(int, message.split())
        if self.turn == 1:
            board = self.board2
            ships = self.ships2
        else:
            board = self.board1
            ships = self.ships1
        if board[x][y] != 0:
            ship = board[x][y]
            ships[ship-1] -= 1
            board[x][y] = -1
            if ships[ship-1] == 0:
                return "Hit and sunk"
            else:
                return "Hit"
        else:
            return "Miss"

    def play_game(self):
        self.place_ships(self.board1, self.ships1)
        self.place_ships(self.board2, self.ships2)
        msg1 = ""
        msg2 = ""
        while not self.game_over:
            if self.turn == 1:
                msg1 = "Your turn"
                msg2 = "Opponent's turn"
                address = self.player1_address
            else:
                msg1 = "Opponent's turn"
                msg2 = "Your turn"
                address = self.player2_address
            bytesToSend = str.encode(msg1)
            UDPServerSocket.sendto(bytesToSend, self.player1_address)
            bytesToSend = str.encode(msg2)
            UDPServerSocket.sendto(bytesToSend, self.player2_address)
            bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
            message = bytesAddressPair[0].decode()
            address = bytesAddressPair[1]
            print("Received message:", message)
            msg = self.get_message(message)
            bytesToSend = str.encode(msg)
            UDPServerSocket.sendto(bytesToSend, address)
            if self.ships1.count(0) == 10:
                self.game_over = True
                bytesToSend = str.encode("You win!")
                UDPServerSocket.sendto(bytesToSend, self.player1_address)
                bytesToSend = str.encode("You lose!")
                UDPServerSocket.sendto(bytesToSend, self.player2_address)
            elif self.ships2.count(0) == 10:
                self.game_over = True
                bytesToSend = str.encode("You win!")
                UDPServerSocket.sendto(bytesToSend, self.player2_address)
                bytesToSend = str.encode("You lose!")
                UDPServerSocket.sendto(bytesToSend, self.player1_address)
            else:
                self.turn = 3 - self.turn

localIP = "127.0.0.1"
localPort = 20001
bufferSize = 1024

# Crear un datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")

games = []

while True:
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    address = bytesAddressPair[1]
    print("Client connected:", address)
    if len(games) == 0 or games[-1].game_over:
        games.append(BattleshipGame(address, None))
        bytesToSend = str.encode("Waiting for opponent")
        UDPServerSocket.sendto(bytesToSend, address)
    else:
        game = games[-1]
        game.player2_address = address
        bytesToSend = str.encode("Game starting")
        UDPServerSocket.sendto(bytesToSend, game.player1_address)
        UDPServerSocket.sendto(bytesToSend, game.player2_address)
        threading.Thread(target=game.play_game).start()
