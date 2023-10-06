class Jugador:
    def __init__(self, address):
        self.address = address
        #self.nombre = nombre
        self.ships = {}
        self.points = 6
        self.opponent = None

    def añadirBarco(self, posiciones):
        self.ships = posiciones

    def asignarOponente(self, oponente):
        self.opponent = oponente

    def obtenerBarcos(self):
        return self.ships.casillas

    def realizarAccion(self, accion):
        pass

class Barcos:
    def __init__(self, barcos):
        tipos = ["p","b","s"]
        tamaños = {"p": 1, "b": 2, "s": 3}
        self.casillas = []
        for tipo in tipos:
            print(barcos[tipo][2] == 1)
            if barcos[tipo][2] == 1: #Horizontal
                for i in range(tamaños[tipo]):
                    print(barcos[tipo][0], barcos[tipo][1] + i)
                    self.casillas.append([barcos[tipo][0], barcos[tipo][1] + i])
                
            else: #Vertical
                self.casillas.append([barcos[tipo][0] + i, barcos[tipo][1]] for i in range(tamaños[tipo]))
        #print("----------------")
        #print (self.casillas)
    def recibirAtaque(self, posicion):
        if posicion in self.casillas:
            self.casillas.remove(posicion)
            return True
        else:
            return False

    def hundir(self):
        pass

class Tablero:
    def __init__(self, tamaño):
        self.tamaño = tamaño
        self.casillas = [[Casilla() for x in range(tamaño)] for y in range(tamaño)]

    def colocarBarco(self, barco, coordenadas):
        pass

    def realizarAtaque(self, coordenada):
        pass

    def barcosHundidos(self):
        pass

    def barcosVivos(self):
        pass

class Servidor:
    def __init__(self):
        self.jugadoresConectados = {}

    def iniciarPartida(self):
        pass

    def finalizarPartida(self):
        pass

class Cliente:
    def __init__(self, nombre):
        self.nombre = nombre
        self.servidor = None

    def conectarAServidor(self, servidor, port):
        self.servidor = servidor
        self.port = port

        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.socket.bind((self.servidor, self.port))
        #mensaje de conexion
        self.socket.sendto("conexion".encode(), (self.servidor, self.port))


    def conectarASala(self, sala):
        pass

    def desconectar(self):
        #mensaje de desconexion
        self.socket.sendto("desconexion".encode(), (self.servidor, self.port))
        self.socket.close()
        pass

    def jugarTurno(self):
        pass

