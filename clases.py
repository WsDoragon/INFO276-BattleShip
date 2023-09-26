class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre


    def realizarAccion(self, accion):
        pass

class Barco:
    def __init__(self, tipo, estado, tamaño):
        self.tipo = tipo
        self.estado = estado
        self.tamaño = tamaño

    def recibirAtaque(self, posicion):
        pass

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
        self.jugadoresConectados = []

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

