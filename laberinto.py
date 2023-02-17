import time
import os
import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)

# ==========================================
#                FUNCIONES
# ==========================================

def changeCurrentCoords(r, c):
    global currentCoords
    currentCoords=(r,c)
    return currentCoords

def changeBannedCoords(r, c):
    global bannedCoords
    bannedCoords.append((r,c))
    return bannedCoords

def establishNewDirectionCoords(r, c):
    global newDirectionCoords
    newDirectionCoords=(r,c)
    return newDirectionCoords

def removeBannedCoordsAndWrongDirections(pathCoords, pathDirections):
    pathCoords.remove(pathCoords[len(pathCoords)-1])
    pathDirections.remove(pathDirections[len(pathDirections)-1])
    changeCurrentCoords(pathCoords[len(pathCoords)-1], pathCoords[len(pathCoords)-1])

def saveCoordsToList(currentCoords, pathCoords):
    pathCoords.append(currentCoords)

def saveDirectionToList(direction, pathDirections):
    pathDirections.append(direction)

def updatePathColour(mazeMatrix, currentCoords):
    mazeMatrix[currentCoords[0]][currentCoords[1]] = Back.YELLOW + "0 "

def updateBannedCoords(mazeMatrix, currentCoords, pathCoords, pathDirections):
    global bannedCoords
    bannedCoords = changeBannedCoords(currentCoords[0],currentCoords[1])
    removeBannedCoordsAndWrongDirections(pathCoords, pathDirections)    
    mazeMatrix[currentCoords[0]][currentCoords[1]] = Back.WHITE + "X "
    changeCurrentCoords(pathCoords[len(pathCoords)-1][0], pathCoords[len(pathCoords)-1][1])
    return bannedCoords

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

def coordsNotBanned(mazeMatrix, newDirectionCoords, bannedCoords):
    if (newDirectionCoords not in bannedCoords):
        return True
    else:
        return False

def coordsNotInCoordList(newDirectionCoords, pathCoords):
    if (newDirectionCoords not in pathCoords):
        return True
    else:
        return False

def canMove(direction, mazeMatrix, pathCoords, pathDirections, currentCoords, bannedCoords):
    global newDirectionCoords
    newDirectionCoords = ()
    newCoord = ()

    right=currentCoords[1]+1
    down=currentCoords[0]+1
    left=currentCoords[1]-1
    up=currentCoords[0]-1

    newRow=currentCoords[0]
    newCol=currentCoords[1]

    if (direction=="Right"):
        newDirectionCoords = establishNewDirectionCoords(newRow, right)
        newColPlus = right
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

    elif (direction=="Down"):
        newDirectionCoords = establishNewDirectionCoords(down, newCol)
        newRowPlus = down
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
        newDirectionCoords = establishNewDirectionCoords(newRow, left)
        newColPlus = left
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
        newDirectionCoords = establishNewDirectionCoords(up, newCol)
        newRowPlus = up        
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
    else:
        bannedCoords = updateBannedCoords(mazeMatrix, currentCoords, pathCoords, pathDirections)
        return True        

# la función createFillMaze crea una matriz dentro de la función y la rellena con el valor "0 " + color negro de fondo en cada posición. Esta matriz es devuelta para poder usarla en el programa principal.
def createAndFillMaze(option):
    # Se crea un array vacío y se indican el número de filas y columnas
    mazeMatrix = []
    global exitCoords

    if (option=="a"):
        row = 4
        col = 5
        background = Back.BLACK + "0 "

        exitCoords = (0,2)

        # Por cada fila se insertan "col" columnas con valor de la variable"background", o sea, el string "0 " con el fondo de color negro.
        for r in range(row):
            mazeMatrix.append([background]*col)

        # Una vez hemos rellenado el laberinto de "0 " ya podemos indicar en que posición se encuentran el Inicio ("I"), la Salida ("S") y los muros (X).
        mazeMatrix[0][0] = "I"  # Inicio
        mazeMatrix[0][2] = "S"  # Final
        mazeMatrix[0][1] = mazeMatrix[2][1], = mazeMatrix[1][2], = mazeMatrix[1][4], = mazeMatrix[2][4], = mazeMatrix[2][2] = "X"  # Muros
    else:
        row = 5
        col = 10
        background = Back.BLACK + "0 "

        exitCoords = (0,9)

        # Por cada fila se insertan "col" columnas con valor de la variable"background", o sea, el string "0 " con el fondo de color negro.
        for r in range(row):
            mazeMatrix.append([background]*col)

        # Una vez hemos rellenado el laberinto de "0 " ya podemos indicar en que posición se encuentran el Inicio ("I"), la Salida ("S") y los muros (X).
        mazeMatrix[0][0] = "I"  # Inicio
        mazeMatrix[0][9] = "S"  # Final
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

while (finished == False):

    if (currentCoords == exitCoords):
        print("¡Has salido de laberinto!")
        finished=True
    else:
        # Por cada vez que el laberinto no sea haya resuelto, o sea, finished == false limpiaremos el terminal y volveremosa imprimir la matriz del laberinto en el estado actual.
        os.system('cls')
        printMaze(mazeMatrix)

    # También imprimiremos las direcciones y coordenadas de la salida, estas se irán actualizando a medida de que se vaya buscando la salida
        print()
        print("Direcciones del camino:", pathDirections)
        print("Coordenadas del camino:", pathCoords)

    moved = False
    i=0

    while (moved == False):
        direction = defaultDirectionsList[i]
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
        


    time.sleep(1) # Esperamos un segundo para ir viendo el recorrido del camino a seguir para poder salir.