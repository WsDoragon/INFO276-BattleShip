def build_board(dimensiones):
    board = []
    for i in range(dimensiones):
        board.append([])
        for j in range(dimensiones):
            board[i].append(0)
    return board

def put_ship(board, ship, x, y, direction):
    if direction == "h":
        for i in range(ship):
            board[x][y+i] = "O"
    elif direction == "v":
        for i in range(ship):
            board[x+i][y] = "O"
    return board

def print_board(board):
    
    for i in range(len(board[0])+1):
        for j in range(len(board[0])+1):
            #agergar numeros a los lados
            if i == 0 and j == 0:
                print(" ", end=" ")
            elif i == 0:
                print(j-1, end=" ")
            elif j == 0:
                print(i-1, end=" ")
            else:
                print(board[i-1][j-1], end=" ")
        print()

def check_ship(board, x, y, ship, direction):
    if direction == "h":
        for i in range(ship):
            # validacion de que el barco no se salga del tablero
            #print (y+i, len(board[0]))
            if y+i >= len(board[0]):
                return True
            if board[x][y+i] == 1:
                return True
    elif direction == "v":
        for i in range(ship):
            if x+i >= len(board[0]):
                return True
            if board[x+i][y] == 1:
                return True
    return False

def build_game(dimensiones):
    board = build_board(dimensiones)
    ships = [["p",1], ["b",2], ["s",3]]
    myShips ={}
    for ship in ships:
        print("|Tablero actual|")
        print("Tamano del barco: ", ship[1])
        print_board(board)
        x = int(input("x: "))
        y = int(input("y: "))
        direction = input("direction: ")
        while check_ship(board, x, y, ship[1], direction):
            print("---------------------")
            print_board(board)
            print("Ya hay un barco en esa posición o sale de los limites del tablero")
            x = int(input("x: "))
            y = int(input("y: "))
            direction = input("direction: ")
        board = put_ship(board, ship[1], x, y, direction)
        myShips[ship[0]] = [x,y, direction == "h"]
        
    print("Tablero final:")
    print_board(board)

    return myShips, board

def attacked(board, x, y):
    if board[x][y] == 0:
        board[x][y] = "*"
        return board,False
    elif board[x][y] == "O":
        board[x][y] = "X"
        return board,True
    else:
        return board,None
    
def attackEnemy(board, x, y, status):
    if status == 0:
        board[x][y] = "*"
        return board,False
    elif status == 1:
        board[x][y] = "X"
        return board,True
    else:
        return board,None