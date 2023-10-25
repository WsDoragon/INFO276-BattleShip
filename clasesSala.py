import random as rand
class Jugador:
    def __init__(self, address):
        self.address = address
        #self.nombre = nombre
        self.ships = {}
        self.points = 6
        self.turn = False
        self.start = False
        self.opponent = None
        self.salaAsignada = None
    
    def setTurn(self, turn):
        self.turn = turn

    def changeTurn(self):
        self.turn = not self.turn

    def getTurn(self):
        return self.turn

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
                for i in range(tamaños[tipo]):
                    self.casillas.append([barcos[tipo][0] + i, barcos[tipo][1]])
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
        self.jugadoresEsperando = {}
        self.jugadoresBot = {}
        self.jugadoresPartida = {}
        self.salas = {1:None, 2:None, 3:None, 4:None, 5:None, 6:None, 7:None, 8:None, 9:None, 10:None}
        self.maxSalas = 10
        self.notUsed = [1,2,3,4,5,6,7,8,9,10]
    
    def crearSala(self):
        salaSelect = rand.choice(self.notUsed)
        self.notUsed.remove(salaSelect)
        self.salas[salaSelect] = Sala(salaSelect)

    def addJugadorEspera(self, jugador):
        self.jugadoresEsperando[jugador.address] = jugador

    def addJugadorPartida(self, jugador):
        self.jugadoresPartida[jugador.address] = jugador

    def addJugadorBot(self, jugador):
        self.jugadoresBot[jugador.address] = jugador

    def iniciarPartida(self):
        pass

    def finalizarPartida(self):
        pass

class Sala:
    def __init__(self, nombre):
        self.nombre = nombre
        self.jugadores = []
        self.maxJugadores = 2
        self.tablero = None
        self.turno = None

    def agregarJugador(self, jugador):
        if len(self.jugadores) < self.maxJugadores:
            self.jugadores.append(jugador)
            return True
        else:
            return False

    def removerJugador(self, jugador):
        if jugador in self.jugadores:
            self.jugadores.remove(jugador)
            return True
        else:
            return False

    def obtenerJugadores(self):
        return self.jugadores

    def obtenerJugador(self, nombre):
        for jugador in self.jugadores:
            if jugador.nombre == nombre:
                return jugador
        return None

    def obtenerTurno(self):
        return self.turno

    def cambiarTurno(self):
        if self.turno == self.jugadores[0]:
            self.turno = self.jugadores[1]
        else:
            self.turno = self.jugadores[0]

    def obtenerTablero(self):
        return self.tablero

    def obtenerNombre(self):
        return self.nombre

    def obtenerMaxJugadores(self):
        return self.maxJugadores

    def obtenerJugadoresConectados(self):
        return len(self.jugadores)

    def obtenerMaxJugadores(self):
        return self.maxJugadores

    def obtenerJugadoresConectados(self):
        return len(self.jugadores)

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

