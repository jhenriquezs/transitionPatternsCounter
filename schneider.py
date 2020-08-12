from collections import deque
import json, itertools, time

#cubo = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]
#cubo = [0,0,0,0,0,0,0,0,0,0,0,0]

# funcion que retorna una lista del tipo de caras que componen al patron.
# input: (patron) lista de 8 elementos con valores 1 y 0
# output: retorna una lista con el tipo de cara de que compone al patron en cada lado de este.

def face_templates(array):
    faces = {}
    faces["front"] = array[0:4]
    faces["left"] = [array[6],array[0],array[4],array[2]]
    faces["right"] = [array[1],array[7],array[3],array[5]]
    faces["top"] = array[2:6]
    faces["back"] = array[4:8]
    faces["bottom"] = [array[6],array[7],array[0],array[1]]
    cube = {}
    for k,v in faces.items():
        nodos = v.count(1)
        template = str(nodos)+" nodos"
        if (nodos == 2 and (v[1] == v[2])):
            template = "2b nodos"
        cube[k] = template
    return cube

# funcion que rota el patron/cubo en direccion hacia abajo
# input: (patron). lista de 8 elementos con valores 1 y 0
# output: (patron rotado hacia abajo). misma lista con valores en posiciones cambiadas.

def turn_down_center(array):
    cola = deque(array)
    cola.rotate(-2)
    return list(cola)

# funcion que rota el patron/cubo hacia la derecha.
# input: (patron). lista de 8 elementos con valores 1 y 0
# output: (patron rotado hacia abajo). misma lista con valores en posiciones cambiadas.
def turn_right_center(array):
    rotation = [array[6],array[0],array[4],array[2],array[5],array[3],array[7],array[1]]
    return rotation


# funcion que rota el patron/cubo para ver si puede encontrar alguna coincidencia con el diccionario de patrones.
# input: (patron, diccionario)
# patron: lista de 8 elementos con valores 1 y 0
# diccionario: lista que contiene un conjunto de patrones en una lista, donde las llaves son la cantidad de nodos activos(valor 1)
# output: retorna el diccionario actualizado, este puede incluir o no el potencial patron dependiendo de si fue considerado valido o no.
def rotation_check_center(array, dict):
    counter = array.count(1)
    if (counter == 0):
        return dict
    ocurr_array = dict[counter]
    if (ocurr_array):
        for i in range(4):
            for j in range(4):
                if (check_cubes(ocurr_array, array)):
                    return dict
                array = turn_right_center(array)
            array = turn_down_center(array)
        array = turn_right_center(array)

        for i in range(2):
            array = turn_down_center(array)
            for j in range(4):
                if (check_cubes(ocurr_array, array)):
                    return dict
                array = turn_right_center(array)
            array = turn_down_center(array)
    # if (validation_faces(array)):
    #     dict[counter].append(array)
    dict[counter].append(array)
    return dict

# Comparacion entre nuestro patron y la lista de patrones.
def check_cubes(big_arr,arr1):
    for arr in big_arr:
        if (arr == arr1):
            return True
    return False

if __name__ == '__main__':
    start = time.time()
    # diccionario que contendra los patrones por cantidad de nodos activos.
    # tipo de dato: (llave,valor) --> (nodos_activos , [patron_1, patron_2, etc...])
    dict = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: []}

    # genera todos los casos posibles para nodos activos, representando el cubo como una lista de 8 elementos.
    # los elementos representan los vertices activos ya sea como 1 = activo y 0 = no activo.
    casos = list(itertools.product([0, 1], repeat=8))
    print("total de casos: ",len(casos))
    contador = 0
    for arr in casos:
        # se compara y se discrimina uno de los potenciales patrones con los ya agregados al diccionario.
        # si no se encuentra en el diccionario y es valido, el diccionario se actualiza incluyendo este nuevo patron.
        rotation_check_center(list(arr), dict)
        contador+=1
        if (contador%10000 == 0):
            print("han ocurrido: "+str(contador)+" casos")
    total = 0
    for k,v in dict.items():
        total+=len(v)
        print(str(k)+ ": " + str(len(v)))
    print("Patrones obtenidos: ",total)
    caras_cont = {"0 nodos":0,"1 nodos":0,"2 nodos":0,"2b nodos":0,"3 nodos":0,"4 nodos":0,}
    arreglo_cubos = []

    # se conforman los patrones con mas caracteristicas -> [string_caras, patron_binario]
    for k,v in dict.items():
        for arr in v:
            cubo = face_templates(arr)
            arreglo_cubos.append((list(cubo.values()), arr))
            lista = set([*cubo.values()])
            for elem in lista:
                caras_cont[elem] += 1
    with open("schneider_patterns.json", "w") as write_file:
        json.dump(arreglo_cubos, write_file)
    end = time.time()
    print("Tiempo de ejecucion: ", (end-start))