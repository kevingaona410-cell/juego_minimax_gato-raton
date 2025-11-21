import random
import copy 


### se agrego al archivo minimax el contenido de toqueteo que incluye la clase minimax para darle ia al gato
################################## Minimax ##################################################
class minimaxgato:

#inicializacion de la clase
    def __init__(self, tamano, trap_pos):
        self.tamano = tamano
        self.tx,self.ty = trap_pos

#movimientos virtuales posibles para el gato    
    def movimiento_gato(self, estado):
        movimientos = {
            "izquierda": (0, -1),
            "abajo": (1, 0),
            "derecha": (0, 1),
            "arriba": (-1, 0),
        }

        posibles_estados = []
        gx, gy = estado["gato"]

        for dx, dy in movimientos.values():
            nuevo_x = gx + dx
            nuevo_y = gy + dy

            if 0 <= nuevo_x < self.tamano and 0 <= nuevo_y < self.tamano:
                nuevo_estado = copy.deepcopy(estado)
                nuevo_estado["gato"] = (nuevo_x, nuevo_y)
                posibles_estados.append(nuevo_estado)

        return posibles_estados
    
    
#movimientos virtuales posibles para el gato    
    def movimiento_raton(self, estado):
        movimientos = {        
            "w": (-1, 0), 
            "a": (0, -1), 
            "s": (1, 0), 
            "d": (0, 1),
            "wa": (-1, -1), 
            "wd": (-1, 1), 
            "sa": (1, -1),
            "sd": (1, 1),
        }

        posibles_estados = []
        rx, ry = estado["raton"]

        for dx, dy in movimientos.values():
            nuevo_x = rx + dx
            nuevo_y = ry + dy

            if 0 <= nuevo_x < self.tamano and 0 <= nuevo_y < self.tamano:
                if (nuevo_x, nuevo_y) == estado["gato"]:
                    continue

                nuevo_estado = copy.deepcopy(estado)
                nuevo_estado["raton"] = (nuevo_x, nuevo_y)
                posibles_estados.append(nuevo_estado)

        return posibles_estados


#euristica para verificar el beneficio del MAX y el MIN
    def euristica(self,estado): 
        gato = estado["gato"]
        raton = estado["raton"]
        trampa = estado["trampa"]

        gx,gy = estado["gato"]
        rx,ry = estado["raton"]
        tx,ty = estado["trampa"]


        if gato == raton:
            return +999
        elif raton == trampa:
            return +5

        distancia_gr = abs(gx - rx) + abs(gy - ry)
        distancia_rt = abs(rx - tx) + abs(ry - ty)

        resultado = 0
        resultado += (100 - distancia_gr)
        resultado += (10 - distancia_rt)

        return resultado
    
    #funcion wrapper 

    def Minimax(self, estado, profundidad, alpha, beta, turno_gato = True):
        if profundidad == 0 or estado == None:
            return self.euristica(estado)
        
        if turno_gato:
            mejor_valor = float("-inf")
            for nuevo_estado in self.movimiento_gato(estado):
                valor = self.Minimax(nuevo_estado, profundidad - 1, alpha, beta, not turno_gato)
                if valor > mejor_valor:
                    mejor_valor = valor    
            
                alpha = max(alpha, valor)
                if beta <= alpha:
                    break
        
            return mejor_valor
        else:
            mejor_valor = float("+inf")
            for nuevo_estado in self.movimiento_raton(estado):
                valor = self.Minimax(nuevo_estado, profundidad - 1, alpha, beta, not turno_gato)
                if valor < mejor_valor:
                    mejor_valor = valor
                
                beta = min(beta, valor)
                if beta <= alpha:
                    break
            return mejor_valor
    
    def mejor_movimiento (self,estado):
        mejor_valor = float("-inf")
        mejor_movimiento = None
        profundidad_futura = 5

        for nuevo_estado in self.movimiento_gato(estado):
            valor = self.Minimax(nuevo_estado, profundidad_futura, float("-inf"), float("+inf"), False)

            if valor > mejor_valor:
                mejor_valor = valor  
                mejor_movimiento = nuevo_estado["gato"]
        return mejor_movimiento
    
############################################## INICIO DEL JUEGO  ##############################################################
print("¡Bienvenido al juego del Gato y el Ratón!")
tam = input("elija el tamano del tablero? ej. 4,5,6...: ")
tamano = int(tam)
tablero = [["🟩 " for _ in range(tamano)] for _ in range(tamano)]

turno = 0
max_turnos = 20
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
jugador = "raton"
jugador_ia = "gato"
print(f"usted es el jugador {jugador}!\n")
print(f"huye del jugador {jugador_ia}\n")

##### Elegir quién empieza####

inicio = random.choice (["raton","raton"])
print(f"Empieza el {inicio}!\n")


############################################ MOVIMIENTOS DEL JUGADOR ######################################################

# Movimiento del gato 
def mover_gato(gato_x, gato_y, direccion, tamano):
    movimientos = {
        "w": (-1, 0),
        "a": (0, -1),
        "s": (1, 0),
        "d": (0, 1),
        }

    if direccion in movimientos:
        dx, dy = movimientos[direccion]
        nuevo_x = gato_x + dx
        nuevo_y = gato_y + dy
        if not (0 <= nuevo_x < tamano and 0 <= nuevo_y < tamano):

            print("Movimiento fuera del tablero.")
            nuevo_x = gato_x - dx
            nuevo_y = gato_y - dy
            return gato_x, gato_y
        
        else:
            return nuevo_x, nuevo_y
        
    else:
        print("Dirección inválida.")
        return gato_x, gato_y
    




# Movimiento del ratón
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
        if not (0 <= nuevo_x < tamano and 0 <= nuevo_y < tamano):

            print("Movimiento fuera del tablero.")
            nuevo_x = raton_x - dx
            nuevo_y = raton_y - dy
            return raton_x, raton_y
        
        elif (nuevo_x,nuevo_y) == (gato_x,gato_y):
            print("Cuidado ahi esta el gato") 
            nuevo_x = raton_x - dx
            nuevo_y = raton_y - dy
            return raton_x,raton_y
        
        else:
            return nuevo_x, nuevo_y
        
#posiciones virtuales del los objetos en el tablero
rx,ry = raton_x ,raton_y
gx, gy = gato_x, gato_y
tx, ty = raton_trap_x, raton_trap_y

#estado del juego en cada turno
estado = {
"raton": (rx,ry),
"gato": (gx,gy),
"trampa": (tx,ty),
"turno_penalizado": False,
}

############################################## BUCLE PRINCIPAL DEL JUEGO ##############################################################
jugar = minimaxgato(tamano, (tx,ty))

turno_actual = inicio
# Verificar si el gato atrapó al ratón
def verificar_estado(gato_x, gato_y, raton_x, raton_y, raton_trap_x, raton_trap_y):    
    if gato_x == raton_x and gato_y == raton_y:
        print("¡El gato atrapó al ratón! 🐱🎉")
        return "gato_gana"
    elif raton_x == raton_trap_x and raton_y == raton_trap_y:
        print("Caíste en la trampa! El ratón pierde 1 turno")
        return "raton_atrapado"

    else:
        return "continuar"
    

    #bucle que repite hasta que la cantidad max de tuernos sea mayor al turno o si no hay un ganador
while turno < max_turnos and not gana:
    print(f"\n Turno {turno + 1} ")
    mostrar_tablero()

    # Actualizar estado real antes de decidir movimientos
    estado["gato"] = (gato_x, gato_y)
    estado["raton"] = (raton_x, raton_y)

    if turno_actual == "gato":

        mov = jugar.mejor_movimiento(estado)
        gato_x, gato_y = mov

    else:
        if raton_atrapado:
            print("El ratón está atrapado este turno 😣")
            raton_atrapado = False
            turno += 1
            turno_actual = "gato"
            continue

        direccion = input("Hacia dónde quiere mover al ratón?: ").lower()
        raton_x, raton_y = mover_raton(raton_x, raton_y, direccion, tamano)

    resultado = verificar_estado(gato_x, gato_y, raton_x, raton_y, raton_trap_x, raton_trap_y)

    if resultado == "gato_gana":
        gana = True
        
    elif resultado == "raton_atrapado":
        raton_atrapado = True
        raton_trap_x = -999
        raton_trap_y = -999

    
    

    turno_actual = "raton" if turno_actual == "gato" else "gato"
    turno += 1

if not gana:
    print("\n🐭💨 ¡El ratón logró escapar del gato! ¡Victoria del ratón!")