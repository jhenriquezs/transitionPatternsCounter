from collections import deque
import json, itertools, time

#cubo = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]
#cubo = [0,0,0,0,0,0,0,0,0,0,0,0]

# funcion que genera plantillas para las caras del patron.
# input: (patron) lista de 8 elementos con valores 1 y 0
# output: retorna una lista con las plantillas de las caras.

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
        template = v
        # si entran a las condiciones, quiere decir que esa cara equivale a una cara sin refinar.
        if (nodos == 2 and v[1] == v[2]):
            template = [0,0,0,0]
        elif(nodos == 1):
            template = [0,0,0,0]
        cube[k] = template
    return cube

# funcion que retorna una lista del tipo de caras que componen al patron.
# input: (patron) lista de 8 elementos con valores 1 y 0
# output: retorna una lista con el tipo de cara de que compone al patron en cada lado de este.

def face_templates_string(array):
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
        # si entra a la condicion, quiere decir que esta cara no se refina.
        if (nodos == 2 and v[1] == v[2]):
            template = "0 nodos"
        elif(nodos == 1):
            template = "0 nodos"
        cube[k] = template
    return cube


# funcion que retorna True si el arreglo se repite en la lista.
def other_face_similar(arr1,lista):
    for arr in lista:
        if (arr[0] == arr1):
            return True
    return False

# rotacion de cara contrareloj
def rotacion_abajo_izq(arr):
    return [arr[1],arr[3],arr[0],arr[2]]

# rotacion de cara en sentido horario.
def rotacion_abajo_der(arr):
    return [arr[2],arr[0],arr[3],arr[1]]

# rotacion del patron hacia abajo a nivel de caras.
def turn_down_face(array):
    left = rotacion_abajo_izq(array[1])
    right = rotacion_abajo_der(array[2])
    new_arr = [array[3],left,right,array[4],array[5],array[0]]
    return new_arr

# cambio de posicion en el arreglo, para la transicion de las caras traseras.
def back_twist(array):
    return [array[3],array[2],array[1],array[0]]

# rotacion del patron hacia la derecha a nivel de caras.
def turn_right_face(array):
    to_back = back_twist(array[2])
    back_to_back = back_twist(array[4])
    top = rotacion_abajo_der(array[3])
    bottom = rotacion_abajo_izq(array[5])
    return [array[1],back_to_back,array[0],top,to_back,bottom]

# cheque de la similitud entre caras segun la rotacion de patrones en base a caras.
def check_face_similar(arr1,lista):
    for arr in lista:
        if (arr[2] == arr1):
            return True
    return False

# funcion que rota el patron/cubo para ver si puede encontrar alguna coincidencia con la lista de patrones.
# input: (patron, lista)
# patron: lista de 18 elementos con valores 1 y 0
# lista: lista que contiene los patrones en formato [caras_binarias, patron_binario, caras_string]
# output: retorna la lista actualizada, este puede incluir o no el potencial patron dependiendo de si fue considerado valido o no.
def rotation_check_face(arr, lista):
    array = arr[2]
    for i in range(4):
        for j in range(4):
            if (check_face_similar(array,lista)):
                print("encontramos que : "+str(array)+" esta repetido")
                return lista
            array = turn_right_face(array)
        array = turn_down_face(array)
    array = turn_right_face(array)

    for i in range(2):
        array = turn_down_face(array)
        for j in range(4):
            if (check_face_similar(array,lista)):
                print("encontramos que : " + str(array) + " esta repetido")
                return lista
            array = turn_right_face(array)
        array = turn_down_face(array)
    lista.append(arr)
    return lista

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

# Comparacion entre nuestro patron y la lista de patrones.
def check_cubes(big_arr,arr1):
    for arr in big_arr:
        if (arr == arr1):
            return True
    return False

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
    dict[counter].append(array)
    return dict


if __name__ == '__main__':
    start = time.time()
    # diccionario que contendra los patrones por cantidad de nodos activos.
    # tipo de dato: (llave,valor) --> (nodos_activos , [patron_1, patron_2, etc...])
    dict = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: []}

    # genera todos los casos posibles para nodos activos, representando el cubo como una lista de 8 elementos.
    # los elementos representan los vertices activos ya sea como 1 = activo y 0 = no activo.
    casos = list(itertools.product([0, 1], repeat=8))
    print("cantidad de casos: ",len(casos))
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
    print("total de patrones: ",total)
    arreglo_cubos = []

    # se conforman los patrones con mas caracteristicas -> [string_caras, patron_binario, caras_binario]
    for k,v in dict.items():
        for arr in v:
            # arreglo con composicion de caras en forma binaria.
            cubo = face_templates(arr)
            # arreglo con composicion de caras como string (se usa en tikz).
            names = face_templates_string(arr)
            arreglo_cubos.append((list(names.values()),arr,list(cubo.values())))
    filtered = []
    # se filtran los patrones similares post actualizacion
    for nuevo in range(len(arreglo_cubos)):
        if (not other_face_similar(arreglo_cubos[nuevo][0],filtered)):
            filtered.append(arreglo_cubos[nuevo])
    print("primer filtro: ",len(filtered))
    new_filter = []
    # se filtran los patrones en base a las caras.
    for filtros in filtered:
        rotation_check_face(filtros,new_filter)
    print("ultimo filtro: ",len(new_filter))

    # se genera un archivo con los datos de los patrones
    with open("ito_patterns.json", "w") as write_file:
         json.dump(new_filter, write_file)
    end = time.time()
    print("Tiempo de ejecucion: ", (end-start))