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

'''
Clase: Servidor
Atributos:
- jugadoresConectados: Lista de Jugadores
Métodos:
- iniciarPartida(): void
- finalizarPartida(): void
'''

class Servidor:
    def __init__(self):
        self.jugadoresConectados = []

    def iniciarPartida(self):
        pass

    def finalizarPartida(self):
        pass

'''
Clase: Cliente
Atributos:
- nombre: String
- servidor: Servidor
Métodos:
- conectarAServidor(servidor: Servidor): void
- desconectar(): void
- jugarTurno(): void
'''

class Cliente:
    def __init__(self, nombre):
        self.nombre = nombre
        self.servidor = None

    def conectarAServidor(self, servidor):
        self.servidor = servidor

    def desconectar(self):
        pass

    def jugarTurno(self):
        pass

