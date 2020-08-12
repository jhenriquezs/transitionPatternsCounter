from collections import deque
import json, itertools, time

# la mayoria de este codigo es similar a gonzalez_octree8.py, solo que presenta ligeros cambios para corroborar los resultados
# y la persepectiva de gonzalez.



# funcion que rota el patron/cubo en direccion hacia abajo
# input: (patron). lista de 18 elementos con valores 1 y 0
# output: (patron rotado hacia abajo). misma lista con valores en posiciones cambiadas.
def turn_down_center(array):
    cola = deque(array[:12])
    cola.rotate(-3)
    newlist = list(cola)
    cola_center = deque(array[12:16])
    cola_center.rotate(-1)
    newlist = newlist+list(cola_center)+array[16:]
    return newlist

# funcion que rota el patron/cubo hacia la derecha.
# input: (patron). lista de 18 elementos con valores 1 y 0
# output: (patron rotado hacia abajo). misma lista con valores en posiciones cambiadas.
def turn_right_center(array):
    rotation = [array[11],array[2],array[8],array[5],array[3],array[6],array[4],array[1],array[7],array[10],array[0],array[9]]
    centros = [array[17],array[13],array[16],array[15],array[12],array[14]]
    return rotation+centros

# Comparacion entre nuestro patron y la lista de patrones.
# input: (lista_de_patrones, patron, patron_original, numero_del_patron).
# lista_de_patrones: lista de listas con 18 elementos con valores 1 y 0.
# patron: lista de 18 elementos con valores 1 y 0 extraido de gonzalez, (este patron puede estar rotado).
# patron_original: lista de 18 elementos con valores 1 y 0. es el patron original obtenido por gonzalez.
# numero_del_patron: es un entero que identifica el patron de gonzalez.
# output: True or False. True si patron esta presente en lista_de_patrones.
def check_cubes(big_arr,arr1,cubo,patron):
    for arr in big_arr:
        # si encuentra la igualdad, retorna true y realiza print para realizar tabla en LaTex.
        if (arr == arr1):
            string = ""
            string2 = ""
            for i in range(len(cubo)):
                if cubo[i] == 1:
                    for k,v in trad.items():
                        if v == i+1:
                            string+= k+", "
            #print(str(arr).replace(" ","") + " & " + str(cubo).replace(" ", "") + " & " + string[:-1] + " \\\ \hline")
            for i in range(len(arr)):
                if arr[i] == 1:
                    string2 += str(i+1) + ", "
            print("\centering "+str(patron) + " & " +string2[:-2] + " & "  + string[:-2] + " \\\ \hline")
            return True
    return False

# funcion que rota los patrones de gonzalez contrastandolos con el conjunto obtenido en archivo .json
# input: (patron_gonzalez, diccionario_patrones, numero_del_patron)

# patron_gonzalez: es una lista de 18 elementos con valores 0 y 1 extraido de los resultados obtenidos por gonzalez.

# diccionario_patrones: es un diccionario donde las llaves son la cantidad de arcos activos y los valores una lista de
# patrones que cumplen con la condicion de la llave. este diccionario es obtenido del gonzalez_octree8.py

# numero_del_patron: es un entero que identifica el patron de gonzalez. ej: patron_gonzalez puede ser el patron numero 105
# de su estudio, por lo tanto, numero_del_patron = 105.
def rotation_check_center(array, dict, patron):
    # guarda el patron original previo a las rotaciones.
    first = array
    counter = array.count(1)
    if (counter == 0):
        return dict
    ocurr_array = dict[str(counter)]
    if (ocurr_array):
        for i in range(4):
            for j in range(4):
                if (check_cubes(ocurr_array, array,first,patron)):
                    return dict
                array = turn_right_center(array)
            array = turn_down_center(array)
        # se rota el patron a la derecha, porque nos falta ver los lados de la izquierda y la derecha del patron,
        # como lados superiores e inferiores.
        array = turn_right_center(array)
        for i in range(2):
            array = turn_down_center(array)
            for j in range(4):
                if (check_cubes(ocurr_array, array,first,patron)):
                    return dict
                array = turn_right_center(array)
            array = turn_down_center(array)
    print("nuevo patron? :o")
    return dict


# Si los print de LaTex se omiten, no debiese existir print alguno.
if __name__ == '__main__':
    # diccionario que contendra los patrones de gonzalez segun la cantidad de nodos/arcos activos.
    dict_arr = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: [], 13: [], 14: [],
                15: [], 16: [], 17: [], 18: []}
    # diccionario que traduce los nodos de gonzalez a los nodos mostrados en la memoria y utilizados en gonzalez_octree8.py
    trad = {'9': 1, '14': 2, '13': 3, '17': 4, '18': 5, '16': 6, '19': 7, '15': 8, '12': 9, '11': 10, '10': 11, '8': 12,
            '22': 13, '25': 14, '24': 15, '20': 16, '23': 17, '21': 18}
    cont = 1
    # abre archivo que contiene los nodos activos en el paper de gonzalez
    file1 = open('resultados.txt', 'r')
    Lines = file1.readlines()
    for line in Lines:
        cubo = line.strip().split(" ")
        if ('26' in cubo):
            # remueve el nodo 26 de gonzalez, que no es significativo para el estudio realizado y que afecta a nuestro conteo.
            cubo.remove('26')
        nodos = len(cubo)
        traduccion = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for elem in cubo:
            traduccion[trad[elem] - 1] = 1
        dict_arr[nodos].append([traduccion, cont])
        cont += 1

    # leemos json, que contiene el diccionario generado en gonzalez_octree8.py, cuyo formato es similar a dict_array
    with open('results_center.json') as json_file:
        data = json.load(json_file)

    # operaciones rotacionales para verificar si los patrones de gonzalez son los mismo que los obtenidos en nuestro otro programa.
    for k,v in dict_arr.items():
        for arr in v:
            rotation_check_center(list(arr[0]), data, arr[1])