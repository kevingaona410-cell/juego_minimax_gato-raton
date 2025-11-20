import random

############################################## INICIO DEL JUEGO  ##############################################################
print("¡Bienvenido al juego del Gato y el Ratón!")

tamano = 4
tablero = [["🟩 " for _ in range(tamano)] for _ in range(tamano)]

turno = 0
max_turnos = 10
gana = False
raton_atrapado = False

# Posiciones iniciales 
gato_x = random.randint(0, tamano - 1)
gato_y = random.randint(0, tamano - 1)
raton_x = random.randint(0, tamano - 1)
raton_y = random.randint(0, tamano - 1)
raton_trap_x = random.randint (0, tamano -1)
raton_trap_y = random.randint (0, tamano -1)

# Calcular distancia mínima entre gato y ratón 
def calcular_distancia(gato_x, gato_y, raton_x, raton_y, distancia_min=4):
    distancia = abs(gato_x - raton_x) + abs(gato_y - raton_y)
    while distancia < distancia_min: #mientras la distancia sea menor reposicionar al raton
        raton_x = random.randint(0, tamano - 1)
        raton_y = random.randint(0, tamano - 1)
        distancia = abs(gato_x - raton_x) + abs(gato_y - raton_y)
    return raton_x, raton_y, distancia


distancia = abs(gato_x - raton_x) + abs(gato_y - raton_y)
if gato_x == raton_x and gato_y == raton_y or distancia < 4:
    raton_x, raton_y, distancia = calcular_distancia(gato_x, gato_y, raton_x, raton_y)


# Mostrar tablero
def mostrar_tablero():
    for x in range(tamano):
        for y in range(tamano):
            if (x, y) == (gato_x, gato_y):
                print("😸 ", end="")
            elif (x, y) == (raton_x, raton_y):
                print("🐭 ", end="")
            elif (x, y) == (raton_trap_x,raton_trap_y) and turno >= 5:
                print ("🪤  ", end="")
            else:
                print("🟩 ", end="")
        print()
    print()
mostrar_tablero()

##### Elegir jugador #####
jugador = input("¿Desea ser el gato o el ratón? (gato/raton): ").lower()
print(f"Has elegido ser el {jugador}!\n")

##### Elegir quién empieza####

#inicio = random.choice ("gato", "raton")
inicio = "jugador"  # por ahora siempre empieza el jugador
print(f"Empieza el {inicio}!\n")


############################################ MOVIMIENTOS DEL JUGADOR ######################################################

# Movimiento del gato (aleatorio por ahora)
def mover_gato(gato_x, gato_y):
    dx = [0, 1, 0, -1]
    dy = [1, 0, -1, 0]
    posibles_mov = []
    for i in range(4):
        new_x = gato_x + dx[i]
        new_y = gato_y + dy[i]
        if 0 <= new_x < tamano and 0 <= new_y < tamano:
            posibles_mov.append((new_x, new_y))
    return random.choice(posibles_mov)


# --- Movimiento del ratón (manual, con diagonales) ---
def mover_raton(raton_x, raton_y, direccion, tamano):
    movimientos = {
        "w": (-1, 0),
        "a": (0, -1),
        "s": (1, 0),
        "d": (0, 1),
        "wa": (-1, -1),
        "wd": (-1, 1),
        "sa": (1, -1),
        "sd": (1, 1),
        "aw": (-1, -1),
        "dw": (-1, 1),
        "as": (1, -1),
        "ds": (1, 1)
    }

    if direccion in movimientos:
        dx, dy = movimientos[direccion]
        nuevo_x = raton_x + dx
        nuevo_y = raton_y + dy
        if 0 <= nuevo_x < tamano and 0 <= nuevo_y < tamano:
            return nuevo_x, nuevo_y
        else:
            print("Movimiento fuera del tablero.")
            return raton_x, raton_y
    else:
        print("Dirección inválida.")
        return raton_x, raton_y


##############################################BUCLE PRINCIPAL DEL JUEGO ##############################################################

    # Verificar si el gato atrapó al ratón
def verificar_estado(gato_x,gato_y,raton_x,raton_y,raton_trap_x,raton_trap_y):    
    if gato_x == raton_x and gato_y == raton_y:
        print("¡El gato atrapó al ratón! 🐱🎉")
        return "gato_gana"
    elif raton_x == raton_trap_x and raton_y == raton_trap_y:
        print("caiste en la trampa de ratones perdiste 1 turno")
        return "raton_atrapado"
    else: 
        return "continuar"
    
while turno < max_turnos and not gana:
    print(f"\n Turno {turno + 1} ")
    mostrar_tablero()

    if jugador == "gato":
        # Mueve el gato (jugador)
        direccion = input("Hacia donde quiere mover al gato?: ").lower()
        if direccion in ["w", "a", "s", "d"]:
            if direccion == "w" and gato_x > 0: gato_x -= 1
            elif direccion == "s" and gato_x < tamano - 1: gato_x += 1
            elif direccion == "a" and gato_y > 0: gato_y -= 1
            elif direccion == "d" and gato_y < tamano - 1: gato_y += 1
        else:
            print("Movimiento inválido.")
    
    else:  
        if raton_atrapado:
            print("El ratón está atrapado este turno 😣")
            raton_atrapado = False
            turno += 1
            continue
        # Mueve el ratón (jugador)
        direccion = input("Hacia donde quiere mover al ratón?: ").lower()
        raton_x, raton_y = mover_raton(raton_x, raton_y, direccion, tamano)

    estado = verificar_estado(gato_x,gato_y,raton_x,raton_y,raton_trap_x,raton_trap_y)

    if estado == "gato_gana":
        gana = True
        break
    elif estado == "raton_atrapado":
        raton_atrapado = True

    turno += 1

if not gana:
    print("¡El ratón ha escapado después de 10 turnos! 🐭💨")



################################## Minimax ##################################################
