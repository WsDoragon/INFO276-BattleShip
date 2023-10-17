import pygame
import random

# Configuración del juego
tamaño_tablero = 5
num_barcos = 3
celda_size = 50
screen_width = tamaño_tablero * celda_size
screen_height = tamaño_tablero * celda_size

# Colores
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)

# Estados del juego
EN_MENU = 0
EN_JUEGO = 1

# Inicializar Pygame
pygame.init()

# Crear la ventana
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Battleship')

# Función para colocar aleatoriamente los barcos en el tablero
def colocar_barcos(tablero, num_barcos):
    for _ in range(num_barcos):
        fila = random.randint(0, tamaño_tablero - 1)
        columna = random.randint(0, tamaño_tablero - 1)
        tablero[fila][columna] = 'B'

# Función para dibujar el tablero
def dibujar_tablero(tablero):
    for fila in range(tamaño_tablero):
        for columna in range(tamaño_tablero):
            color = white
            if tablero[fila][columna] == 'X':
                color = red
            elif tablero[fila][columna] == 'O':
                color = blue
            pygame.draw.rect(screen, color, (columna * celda_size, fila * celda_size, celda_size, celda_size), 0)
            pygame.draw.rect(screen, (0, 0, 0), (columna * celda_size, fila * celda_size, celda_size, celda_size), 1)

# Función para manejar el clic en una celda
def clic_celda(fila, columna):
    if tablero[fila][columna] == 'B':
        tablero[fila][columna] = 'X'
    else:
        tablero[fila][columna] = 'O'

# Funciones para los modos de juego
def contra_cpu():
    iniciar_juego()
    # Lógica del modo contra CPU

def contra_un_usuario():
    iniciar_juego()
    # Lógica del modo contra 1 usuario

def contra_multiples():
    iniciar_juego()
    # Lógica del modo contra múltiples jugadores

# Función para iniciar el juego
def iniciar_juego():
    global estado
    estado = EN_JUEGO
    reiniciar_juego()

# Función para reiniciar el juego
def reiniciar_juego():
    for fila in range(tamaño_tablero):
        for columna in range(tamaño_tablero):
            tablero[fila][columna] = ' '
    colocar_barcos(tablero, num_barcos)

# Estado inicial
estado = EN_MENU

# Crear el tablero de juego
tablero = [[' ' for _ in range(tamaño_tablero)] for _ in range(tamaño_tablero)]

# Crear el menú principal
font = pygame.font.Font(None, 36)
menu_principal = [
    ("Contra CPU", contra_cpu),
    ("Contra 1 Usuario", contra_un_usuario),
    ("Contra Múltiples", contra_multiples)
]
menu_y = screen_height // 2 - len(menu_principal) * 20

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if estado == EN_MENU and menu_y < event.pos[1] < menu_y + len(menu_principal) * 40:
                for i, (text, callback) in enumerate(menu_principal):
                    if menu_y + i * 40 < event.pos[1] < menu_y + (i + 1) * 40:
                        callback()
            elif estado == EN_JUEGO:
                fila = event.pos[1] // celda_size
                columna = event.pos[0] // celda_size
                if 0 <= fila < tamaño_tablero and 0 <= columna < tamaño_tablero:
                    clic_celda(fila, columna)

    screen.fill(white)

    if estado == EN_MENU:
        # Dibujar menú principal
        for i, (text, _) in enumerate(menu_principal):
            label = font.render(text, True, (0, 0, 0))
            screen.blit(label, (screen_width // 2 - 70, menu_y + i * 40))
    elif estado == EN_JUEGO:
        if all(cell == 'X' for row in tablero for cell in row):
            # Juego ganado
            texto_ganador = font.render("¡Ganaste!", True, red)
            screen.blit(texto_ganador, (screen_width // 2 - 70, screen_height // 2 - 20))
        else:
            dibujar_tablero(tablero)

    pygame.display.flip()

pygame.quit()
