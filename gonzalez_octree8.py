from collections import deque
import json, itertools, time

#cubo = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]
#cubo = [0,0,0,0,0,0,0,0,0,0,0,0]

# funcion que verifica si las caras del patron son validas.
# input: (patron) lista de 18 elementos con valores 1 y 0
# output: (True or False) retorna False si alguna cara no es valida.
def validation_faces(array):
    # establece las caras donde el nodo del centro es el ultimo valor de la lista
    bottom_face = array[9:12]+array[0:1]+array[15:16]
    left_side = [array[2],array[5],array[8],array[11],array[17]]
    right_side = [array[1],array[4],array[7],array[10],array[16]]
    faces = [array[0:4]+array[12:13],array[3:7]+array[13:14],array[6:10]+array[14:15]]
    faces.append(bottom_face)
    faces.append(left_side)
    faces.append(right_side)
    for cara in faces:
        # si el ultimo valor de la lista que representa a la cara es 1 y no estan los 5 nodos activos, retorna falso
        if (cara[-1] == 1 and cara.count(1)!=5):
            return False
    return True

# funcion que rota el patron/cubo en direccion hacia abajo
# input: (patron). lista de 18 elementos con valores 1 y 0
# output: (patron rotado hacia abajo). misma lista con valores en posiciones cambiadas.
def turn_down_center(array):
    # se rotan los arcos del patron conforme a las posiciones indicadas en la memoria.
    cola = deque(array[:12])
    cola.rotate(-3)
    newlist = list(cola)
    # se rotan los centros del patron, excepto los del lado izquierdo y derecho, dado a que su posicion no cambia.
    cola_center = deque(array[12:16])
    cola_center.rotate(-1)
    # concatenamos las colas y listas para generar nuestro patron rotado.
    newlist = newlist+list(cola_center)+array[16:]
    return newlist

# funcion que rota el patron/cubo hacia la derecha.
# input: (patron). lista de 18 elementos con valores 1 y 0
# output: (patron rotado hacia abajo). misma lista con valores en posiciones cambiadas.
def turn_right_center(array):
    # rotacion de centros y arcos segun las posiciones indicadas en la memoria
    rotation = [array[11],array[2],array[8],array[5],array[3],array[6],array[4],array[1],array[7],array[10],array[0],array[9]]
    centros = [array[17],array[13],array[16],array[15],array[12],array[14]]
    return rotation+centros

# Comparacion entre nuestro patron y la lista de patrones.
# input: (lista_de_patrones, patron).
# lista_de_patrones: lista de listas con 18 elementos con valores 1 y 0.
# patron: lista de 18 elementos con valores 1 y 0
# output: True or False. True si patron esta presente en lista_de_patrones.
def check_cubes(big_arr,arr1):
    for arr in big_arr:
        if (arr == arr1):
            return True
    return False

# funcion que rota el patron/cubo para ver si puede encontrar alguna coincidencia con el diccionario de patrones.
# input: (patron, diccionario)
# patron: lista de 18 elementos con valores 1 y 0
# diccionario: lista que contiene un conjunto de patrones en una lista, donde las llaves son la cantidad de nodos activos(valor 1)
# output: retorna el diccionario actualizado, este puede incluir o no el potencial patron dependiendo de si fue considerado valido o no.

def rotation_check_center(array, dict):
    # contamos la cantidad de elementos 1 presentes en la lista que representa al potencial patron.
    counter = array.count(1)
    if (counter == 0):
        return dict
    # se carga la lista de patrones obtenidos para la cantidad de nodos activos.
    ocurr_array = dict[counter]
    # se procede a rotar el potencial patron, para ver si es similar a los patrones entregados por el diccionario.
    if (ocurr_array):
        for i in range(4):
            for j in range(4):
                if (check_cubes(ocurr_array, array)):
                    return dict
                array = turn_right_center(array)
            array = turn_down_center(array)
        # se rota el patron a la derecha, porque nos falta ver los lados de la izquierda y la derecha del patron,
        # como lados superiores e inferiores.
        array = turn_right_center(array)
        for i in range(2):
            array = turn_down_center(array)
            for j in range(4):
                if (check_cubes(ocurr_array, array)):
                    return dict
                array = turn_right_center(array)
            array = turn_down_center(array)
    # se realiza validacion de las caras para el potencial patron, ya que puede considerar el nodo central de la cara como
    # activo, pero para que este sea valido, tienen que estar los 4 nodos de los arcos activos.
    if (validation_faces(array)):
        dict[counter].append(array)
    return dict


if __name__ == '__main__':
    start = time.time()
    # diccionario que contendra los patrones por cantidad de nodos activos.
    # tipo de dato: (llave,valor) --> (nodos_activos , [patron_1, patron_2, etc...])
    dict = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: [], 13:[], 14:[], 15:[], 16:[], 17:[], 18:[]}

    # genera todos los casos posibles para nodos activos, representando el cubo como una lista de 18 elementos.
    # los elementos representan los nodos activos ya sea como 1 = activo y 0 = no activo.
    # los primeros 12 elementos [0,...,11] representan las aristas del cubo, como se observa en el dibujo de la memoria.
    # el resto de los elementos [12,...,18] representan los nodos del centro de las caras, tambien representado en el dibujo de la memoria.
    # el total de casos se puede sacar como 2^(repeat) en este caso es 2^18.
    casos = list(itertools.product([0, 1], repeat=18))
    print("length: ",len(casos))
    contador = 0
    for arr in casos:
        # se compara y se discrimina uno de los potenciales patrones con los ya agregados al diccionario.
        # si no se encuentra en el diccionario y es valido, el diccionario se actualiza incluyendo este nuevo patron.
        rotation_check_center(list(arr), dict)
        contador+=1
        if (contador%10000 == 0):
            print("han ocurrido: "+str(contador)+" casos")
    total = 0
    # print de total de patrones por nodos activos.
    for k,v in dict.items():
        total+=len(v)
        print(str(k)+ ": " + str(len(v)))
    print(total)
    # guarda el diccionario en un archivo .json
    with open("results_center.json", "w") as write_file:
        json.dump(dict, write_file)
    end = time.time()
    print("Tiempo de ejecucion: ", (end-start))