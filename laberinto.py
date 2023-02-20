import time
import os
import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)

# ==========================================
#                FUNCIONES
# ==========================================

# Función que cambia el valor de la tupla currentCoords por los valores de los parámetros. Devolvemos la variable currentCoords.
def changeCurrentCoords(r, c):
    global currentCoords
    currentCoords=(r,c)
    return currentCoords

# Función que añade a la lista bannedCoords una tupla con los valores de los parámetros. Devolvemos la lista de tuplas bannedCoords.
def changeBannedCoords(r, c):
    global bannedCoords
    bannedCoords.append((r,c))
    return bannedCoords

# Función que cambia el valor de la tupla newDirectionCoords por los valores de los parámetros. Esta tupla nos sirve para guardar la posición a la que nos queremos mover en el laberinto y más tarde comprobar
#  i podemos movernos a esa posición. Devolvemos la variable currentCoords.
def establishNewDirectionCoords(r, c):
    global newDirectionCoords
    newDirectionCoords=(r,c)
    return newDirectionCoords

# Esta función se usará cuando estemos sin salida para eliminar la última posición de la lista de coordenadas y lista de direcciones, y después de borrar la última posición de 
# pathCoords poder cambiar el valor de de currentCoords a la nueva última posición de pathCoords. 
def removeBannedCoordsAndWrongDirections(pathCoords, pathDirections):
    pathCoords.remove(pathCoords[len(pathCoords)-1])
    pathDirections.remove(pathDirections[len(pathDirections)-1])
    changeCurrentCoords(pathCoords[len(pathCoords)-1], pathCoords[len(pathCoords)-1])

# Guardamos la posición de las coordenadas actuales en la lista de pathCoords, está lista se irá actualizando y mostrando a medida de que se recorre el laberinto.
def saveCoordsToList(currentCoords, pathCoords):
    pathCoords.append(currentCoords)

# Igual que con saveDirectionToList guardaremos direction en pathDirections y lo mostraremos a medida de que se recorre el laberinto.
def saveDirectionToList(direction, pathDirections):
    pathDirections.append(direction)

# Una simple función para cambiar el color de la "casilla" a la cual nos hemos movido
def updatePathColour(mazeMatrix, currentCoords):
    mazeMatrix[currentCoords[0]][currentCoords[1]] = Back.YELLOW + "0 "

# Cuando nos encontremos ante un callejón sin salida deberemos usar esta función para: 
def updateBannedCoords(mazeMatrix, currentCoords, pathCoords, pathDirections):
    global bannedCoords
    bannedCoords = changeBannedCoords(currentCoords[0],currentCoords[1]) # Guardar la posición del callejón sin salida en bannedCoords, una lista de tuplas.
    removeBannedCoordsAndWrongDirections(pathCoords, pathDirections) # Deberemos eliminar la posición y dirección anterior que hayamos guardado en pathDirections y pathCoords respectivamente  
    mazeMatrix[currentCoords[0]][currentCoords[1]] = Back.WHITE + "X " # Actualizamos el carácter y el color de la posición que representa un callejón sin salida.
    changeCurrentCoords(pathCoords[len(pathCoords)-1][0], pathCoords[len(pathCoords)-1][1]) # Y finalmente cambiamos las currentCoords a la última posición de pathCoords.
    return bannedCoords

# Con esta función comprobamos si la coordenada activa (la fila o columna que representa el movimiento, o sea, vale +1) es una columna o fila ya que deberemos su longitud es distinta.
# Una vez sepamos si es columna o fila nos dispondremos a comprobar si se encuentra dentro de las medidas de la matriz, si lo está devolveremos True, si no False.
def coordsInBounds(mazeMatrix, newCoord, posType):
    if (posType == "Column"):
        if (0 <= (newCoord) < len(mazeMatrix[0])):
            return True
        else:
            return False
    elif (posType == "Row"):
        if (0 <= (newCoord) < len(mazeMatrix)):
            return True
        else:
            return False

# Con esta función queremos saber primero si se trata de una columna o fila y una vez sepamos eso comprobaremos si esa posición dentro de la matriz es un muro, si lo es devolveremos False, si no True.
def coordsNotAWall(mazeMatrix, otherCoord, newCoord, posType):
    if (posType == "Column"):
        if (mazeMatrix[otherCoord][newCoord] != Back.RED + "X "):
            return True
        else:
            return False
    elif (posType == "Row"):
        if (mazeMatrix[newCoord][otherCoord] != Back.RED + "X "):
            return True
        else:
            return False

# Simplemente comprobamos si las newDirectionCoords (una tupla con la columna y fila a la que nos queremos desplazar) se encuentran en la lista de tuplas bannedCoords.
def coordsNotBanned(mazeMatrix, newDirectionCoords, bannedCoords):
    if (newDirectionCoords not in bannedCoords):
        return True
    else:
        return False

# Ya que podemos llegar a la situación de recorrer el mismo camino una y otra vez, debemos comprobar si las newDirectionCoords (una tupla con la columna y fila a la que nos queremos desplazar)
# se encuentran en la lista de pathCoords. Si lo está significa que ya hemos recorrido esa posición así que nos devolverá False, si no la hemos recorrido devolvería True.
def coordsNotInCoordList(newDirectionCoords, pathCoords):
    if (newDirectionCoords not in pathCoords):
        return True
    else:
        return False

# Esta función es la encargada de comprobar si nos podemos mover hacia una posición en concreto:
def canMove(direction, mazeMatrix, pathCoords, pathDirections, currentCoords, bannedCoords):
    global newDirectionCoords
    newDirectionCoords = () # Tupla que guarda la coordenada al a que nos queremos desplazar.

# newRow y newCol son dos variables que guardan el valor de la fila y columna respectivamente que forma parte de la coordenada a la que nos queremos mover.
    newRow=currentCoords[0]
    newCol=currentCoords[1]

# Esta función consiste de un conjunto de 4 ifs y un else los cuales mirarán si nos podemos desplazar a la derecha, abajo, izquierda, arriba o si nos encontramos sin salida:
    if (direction=="Right"):
        newColPlus = currentCoords[1]+1 # newColPlus es la coordenada columna hacia donde queremos movernos.
        newDirectionCoords = establishNewDirectionCoords(newRow, newColPlus) # Establecemos newDirectionCoords con las coordenadas de newRow y newColPlus para así tener ambas coordenadas juntas en una tupla.
        posType = "Column"

# Si la coordenada se encuentra en los límites de la matriz Y las coordenadas nos son un muro Y las coordenadas no están vetadas (callejón sin salida) Y las coordenadas no están en la lista de coordenadas (ya hemos pasado por esas coordenadas):
        if (coordsInBounds(mazeMatrix, newColPlus, posType) == True  and
            coordsNotAWall(mazeMatrix, newRow, newColPlus, posType) == True and
            coordsNotBanned(mazeMatrix, newDirectionCoords, bannedCoords) == True and
            coordsNotInCoordList(newDirectionCoords, pathCoords) == True):

# Actualizamos currentCoords con las nuevas coordenadas, actualizamos el color del camino a amarillo para indicar que nos hemos movido hacia allí, y guardamos tanto las coordenadas como la dirección en sus respectivas listas.abs(x)
            currentCoords = changeCurrentCoords(newRow, newColPlus)
            updatePathColour(mazeMatrix, currentCoords)
            saveCoordsToList(currentCoords, pathCoords)
            saveDirectionToList(direction, pathDirections)                    
            return True
        else:
            return False
# Devolveremos True o False en función de si cumple o no las condiciones.

    elif (direction=="Down"):
        newRowPlus = currentCoords[0]+1
        newDirectionCoords = establishNewDirectionCoords(newRowPlus, newCol)
        posType = "Row"


        if (coordsInBounds(mazeMatrix, newRowPlus, posType) == True  and
            coordsNotAWall(mazeMatrix, newCol, newRowPlus, posType) == True and
            coordsNotBanned(mazeMatrix, newDirectionCoords, bannedCoords) == True and
            coordsNotInCoordList(newDirectionCoords, pathCoords) == True):

            currentCoords = changeCurrentCoords(newRowPlus, newCol)
            updatePathColour(mazeMatrix, currentCoords)
            saveCoordsToList(currentCoords, pathCoords)
            saveDirectionToList(direction, pathDirections)
            return True
        else:
            return False            

    elif (direction=="Left"):
        newColPlus = currentCoords[1]-1
        newDirectionCoords = establishNewDirectionCoords(newRow, newColPlus)
        posType = "Column"
        

        if (coordsInBounds(mazeMatrix, newColPlus, posType) == True  and
            coordsNotAWall(mazeMatrix, newRow, newColPlus, posType) == True and
            coordsNotBanned(mazeMatrix, newDirectionCoords, bannedCoords) == True and
            coordsNotInCoordList(newDirectionCoords, pathCoords) == True):

            currentCoords = changeCurrentCoords(newRow, newColPlus)
            updatePathColour(mazeMatrix, currentCoords)
            saveCoordsToList(currentCoords, pathCoords)
            saveDirectionToList(direction, pathDirections)
            return True
        else:
            return False

    elif (direction=="Up"):
        newRowPlus = currentCoords[0]-1        
        newDirectionCoords = establishNewDirectionCoords(newRowPlus, newCol)
        posType = "Row"


        if (coordsInBounds(mazeMatrix, newRowPlus, posType) == True  and
            coordsNotAWall(mazeMatrix, newCol, newRowPlus, posType) == True and
            coordsNotBanned(mazeMatrix, newDirectionCoords, bannedCoords) == True and
            coordsNotInCoordList(newDirectionCoords, pathCoords) == True):

            currentCoords = changeCurrentCoords(newRowPlus, newCol)
            updatePathColour(mazeMatrix, currentCoords)
            saveCoordsToList(currentCoords, pathCoords)
            saveDirectionToList(direction, pathDirections)
            return True
        else:
            return False

# En el caso que no nos podamos mover ni a la derecha, abajo, izquierda, arriba significará que nos encontramos en un callejón sin salida, por lo tanto deberemos usar la función updateBannedCoords para
# actualizar la lista de tuplas bannedCoords donde se encuentran todas las posición vetadas.
    else:
        bannedCoords = updateBannedCoords(mazeMatrix, currentCoords, pathCoords, pathDirections)
        return True        

# la función createFillMaze crea una matriz dentro de la función y la rellena con el valor "0 " + color negro de fondo en cada posición. Esta matriz es devuelta para poder usarla en el programa principal.
def createAndFillMaze(option):
    # Se crea un array vacío y se indican el número de filas y columnas
    mazeMatrix = []
    global exitCoords

    # Este programa incluye dos laberintos, uno de 5x4 y otro de 10x5, por lo tanto primero deberemos elegir cual queremos (a o b)
    if (option=="a"):
        row = 4
        col = 5
        background = Back.BLACK + "0 "

        exitCoords = (0,2) # Las coordenadas que indican el final del laberinto

        # Por cada fila se insertan "col" columnas con valor de la variable"background", o sea, el string "0 " con el fondo de color negro.
        for r in range(row):
            mazeMatrix.append([background]*col)

        # Una vez hemos rellenado el laberinto de "0 " ya podemos indicar en que posición se encuentran el Inicio ("I"), la Salida ("S") y los muros (X).
        mazeMatrix[0][0] = "I"  # Inicio
        mazeMatrix[exitCoords[0]][exitCoords[1]] = "S"  # Final
        mazeMatrix[0][1] = mazeMatrix[2][1], = mazeMatrix[1][2], = mazeMatrix[1][4], = mazeMatrix[2][4], = mazeMatrix[2][2] = "X"  # Muros
    else:
        row = 5
        col = 10
        background = Back.BLACK + "0 "

        exitCoords = (0,2)

        # Por cada fila se insertan "col" columnas con valor de la variable"background", o sea, el string "0 " con el fondo de color negro.
        for r in range(row):
            mazeMatrix.append([background]*col)

        # Una vez hemos rellenado el laberinto de "0 " ya podemos indicar en que posición se encuentran el Inicio ("I"), la Salida ("S") y los muros (X).
        mazeMatrix[0][0] = "I"  # Inicio
        mazeMatrix[exitCoords[0]][exitCoords[1]] = "S"  # Final
        mazeMatrix[0][1] = mazeMatrix[2][1], = mazeMatrix[1][2], = mazeMatrix[1][4], = mazeMatrix[2][4], = mazeMatrix[2][2], = mazeMatrix[4][0], = mazeMatrix[4][2], = mazeMatrix[4][3], = mazeMatrix[4][4], = mazeMatrix[4][5], = mazeMatrix[4][6], = mazeMatrix[3][6], = mazeMatrix[2][6], = mazeMatrix[0][6], = mazeMatrix[0][5], = mazeMatrix[0][4], = mazeMatrix[1][8], = mazeMatrix[1][9], = mazeMatrix[4][8], = mazeMatrix[3][8] = "X" # Muros
    

    formatMaze(mazeMatrix)

    # Devolvemos la matriz para poder usarla en el programa principal
    return mazeMatrix

# La función formatMaze() es una función que no devuelve nada, en cambio sirve para dar formato (con colorama) a las "casillas" previamente introducidas en la matriz del laberinto.
def formatMaze(mazeMatrix):

    # Empezamos recorriendo la matriz y si nos encontramos que mazeMatrix = "X" le daremos el valor de "X " con fondo rojo, y lo mismo con el Inicio y Salida pero con fondo verde.
    for r in range(len(mazeMatrix)):
        for c in range(len(mazeMatrix[r])):
            if mazeMatrix[r][c] == "X":
                mazeMatrix[r][c] = Back.RED + "X "
            elif mazeMatrix[r][c] == "I":
                mazeMatrix[r][c] = Back.GREEN + "I "
            elif mazeMatrix[r][c] == "S":
                mazeMatrix[r][c] = Back.GREEN + "S "

# printMaze(mazeMatrix) sirve para imprimir por pantalla el laberinto pasado por parámetro.
def printMaze(mazeMatrix):
    # La variable r hace referencia a las filas (rows) y la viariable c a las columnas (columns).
    for r in range(len(mazeMatrix)):
        for c in range(len(mazeMatrix[r])):
            print(mazeMatrix[r][c], end="") # Dentro del print se usa el end="" para poder imprimir los valores de la matriz de una fila en una misma línea.
        print() # Después de imprimir todos los valores que se encuentran en una fila hacemos un print normal vacío para cambiar de línea.






# ==========================================
#            PROGRAMA PRINCIPAL
# ==========================================
os.system('cls')

# lista donde guardamos todas las direcciones posibles a las que nos podemos mover, incluyendo la posibilidad de quedarnos sin salida.
defaultDirectionsList = ("Right", "Down", "Left", "Up", "NoExit")

# Creamos dos listas, una para almacenar la dirección que debemos salir para salir del laberinto (pathDirections) y otra para almacenar las coordenadas para el mismo propósito.
pathDirections = ["Inicio"]
pathCoords = [(0,0)]
bannedCoords = []
currentCoords = pathCoords[0]
exitCoords = ()

finished = False # Booleano que permite la finalización del laberinto.
unkownOption = True

print("Puede escoger entre dos laberintos distintos, el a (5x4) o el b (10x5).")
print()

while (unkownOption == True):
    option=input("Indique qué laberinto quiere recorrer (a o b): ")

    if (option != "a" and option != "b"):
        print("La opción que ha escogido no existe. Debe escoger entre la opción a o b.")
    else:
        unkownOption = False

mazeMatrix = createAndFillMaze(option)

# Mientras no hayamos acabado el laberinto (finished==false), el siguiente bucle while se seguirá repetiendo.
while (finished == False):

# Si se da el caso en el que las coordenadas actuales son las mismas que las coordenadas de la salida significa que hemos salido del laberinto, por lo tanto finished es igual a True.
    if (currentCoords == exitCoords):
        print()
        print("¡Has salido de laberinto!")
        print()
        finished=True
    else:
        # Por cada vez que el laberinto no sea haya resuelto, o sea, finished == false limpiaremos el terminal y volveremosa imprimir la matriz del laberinto en el estado actual.
        os.system('cls')
        printMaze(mazeMatrix)

    # También imprimiremos las direcciones y coordenadas de la salida, estas se irán actualizando a medida de que se vaya buscando la salida
        print()
        print("Direcciones del camino:", pathDirections)
        print("Coordenadas del camino:", pathCoords)


    moved = False # El booleano moved nos permitirá salir del bucle si nos hemos movido hacia alguna dirección.
    i=0

    while (moved == False):
        direction = defaultDirectionsList[i] # Usamos la variable i para recorrer la lista de direcciones predeterminadas para ir dando valor a direction para que así vaya probando todas las direcciones.
        if (direction == "Right"):
            moved = canMove(direction, mazeMatrix, pathCoords, pathDirections, currentCoords, bannedCoords)    
        elif (direction == "Down"):
            moved = canMove(direction, mazeMatrix, pathCoords, pathDirections, currentCoords, bannedCoords)
        elif (direction == "Left"):
            moved = canMove(direction, mazeMatrix, pathCoords, pathDirections, currentCoords, bannedCoords)
        elif (direction == "Up"):
            moved = canMove(direction, mazeMatrix, pathCoords, pathDirections, currentCoords, bannedCoords)
        elif (direction == "NoExit"):
            moved = canMove(direction, mazeMatrix, pathCoords, pathDirections, currentCoords, bannedCoords)
        i=i+1
        


    time.sleep(0.3) # Esperamos 0.3 segundos para ir viendo el recorrido del camino a seguir para poder salir.