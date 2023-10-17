import pygame

# Configuración del juego
tamaño_tablero = 5
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

# Tipos de barcos (largo, ancho)
barcos = [(1, 1), (1, 2), (1, 4)]

# Inicializar Pygame
pygame.init()

# Crear la ventana
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Battleship')

# Función para dibujar el tablero
def dibujar_tablero(tablero):
    for fila in range(tamaño_tablero):
        for columna in range(tamaño_tablero):
            color = white
            pygame.draw.rect(screen, color, (columna * celda_size, fila * celda_size, celda_size, celda_size), 0)
            pygame.draw.rect(screen, (0, 0, 0), (columna * celda_size, fila * celda_size, celda_size, celda_size), 1)

# Función para dibujar un barco en el tablero
def dibujar_barco(tablero, fila, columna, largo, ancho, color):
    for i in range(fila, fila + largo):
        for j in range(columna, columna + ancho):
            tablero[i][j] = color

# Función para borrar un barco del tablero
def borrar_barco(tablero, fila, columna, largo, ancho):
    for i in range(fila, fila + largo):
        for j in range(columna, columna + ancho):
            tablero[i][j] = ' '

# Función para manejar el clic en una celda
def clic_celda(fila, columna):
    global barco_seleccionado, barco_rotado
    if estado == EN_MENU:
        pass  # Espera a que los barcos se coloquen
    elif estado == EN_JUEGO:
        if barco_seleccionado:
            fila, columna = fila // celda_size, columna // celda_size
            largo, ancho = barco_seleccionado
            if 0 <= fila < tamaño_tablero - largo + 1 and 0 <= columna < tamaño_tablero - ancho + 1:
                if valida_posicion(tablero, fila, columna, largo, ancho):
                    dibujar_barco(tablero, fila, columna, largo, ancho, blue)
                    barcos.remove(barco_seleccionado)
                    if not barcos:
                        iniciar_juego()
                barco_seleccionado = None

# Función para validar si una posición es válida para colocar un barco
def valida_posicion(tablero, fila, columna, largo, ancho):
    for i in range(fila, fila + largo):
        for j in range(columna, columna + ancho):
            if tablero[i][j] != ' ':
                return False
    return True

# Función para rotar un barco
def rotar_barco():
    global barco_seleccionado
    if barco_seleccionado:
        largo, ancho = barco_seleccionado
        barco_seleccionado = (ancho, largo)

# Función para iniciar el juego
def iniciar_juego():
    global estado
    estado = EN_JUEGO

# Estado inicial
estado = EN_MENU
barco_seleccionado = None  # Barco seleccionado para colocar
barco_rotado = False  # Indica si el barco seleccionado está rotado o no

# Crear el tablero de juego
tablero = [[' ' for _ in range(tamaño_tablero)] for _ in range(tamaño_tablero)]

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if estado == EN_MENU:
                pass  # Permite a los jugadores colocar los barcos
            elif estado == EN_JUEGO:
                clic_celda(event.pos[1], event.pos[0])
        elif event.type == pygame.KEYDOWN:
            if estado == EN_MENU:
                if event.key == pygame.K_SPACE:
                    iniciar_juego()
            elif estado == EN_JUEGO:
                if event.key == pygame.K_SPACE:
                    if barco_seleccionado:
                        fila, columna = pygame.mouse.get_pos()
                        clic_celda(fila, columna)
                elif event.key == pygame.K_r:
                    rotar_barco()

    screen.fill(white)

    if estado == EN_MENU:
        # Dibujar mensaje de inicio
        font = pygame.font.Font(None, 36)
        texto_inicio = font.render("Haz clic en las celdas para colocar tus barcos", True, (0, 0, 0))
        screen.blit(texto_inicio, (10, 10))
    elif estado == EN_JUEGO:
        dibujar_tablero(tablero)
        if barco_seleccionado:
            fila, columna = pygame.mouse.get_pos()
            largo, ancho = barco_seleccionado
            if not barco_rotado:
                pygame.draw.rect(screen, blue, (columna - ancho * celda_size // 2, fila - largo * celda_size // 2,
                                               ancho * celda_size, largo * celda_size), 2)
            else:
                pygame.draw.rect(screen, blue, (columna - largo * celda_size // 2, fila - ancho * celda_size // 2,
                                               largo * celda_size, ancho * celda_size), 2)

    pygame.display.flip()

pygame.quit()
