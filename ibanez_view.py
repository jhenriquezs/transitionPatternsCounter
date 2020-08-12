from collections import deque
import json, itertools, time

# funcion que discrimina si el patron es valido o no segun los estandares del paper de Ito.
# input: (patron). lista de 12 elementos con valores 1 y 0
# output: (True or False) retorna Falso si no cumple con los estandares previamente mencionados.
def face_validation(array):
    # establecemos las caras. segun lo dicho en la memoria. el ORDEN es primordial!!!!!
    # las caras se ordenan como si se observaran de frente, excepto la cara trasera que es la ultima lista de la variable
    # faces. La perspectiva tomada es como si se observase el cubo de frente NO LA CARA DE FRENTE.
    faces = [array[0:4],array[3:7],[array[9], array[7], array[8], array[6]]]
    bottom_face = array[9:12]+array[0:1]
    left_side = [array[11], array[2], array[8], array[5]]
    right_side = [array[1], array[4], array[7], array[10]]
    faces.append(bottom_face)
    faces.append(left_side)
    faces.append(right_side)
    for cara in faces:
        unos = cara.count(1)
        # confirma si presenta arcos activos paralelos o 3 arcos activos.
        if (unos==2 and (cara[0] == cara[3])):
            return False
        if (unos==3):
            return False
    return True

# funcion que rota el patron/cubo en direccion hacia abajo
# input: (patron). lista de 12 elementos con valores 1 y 0
# output: (patron rotado hacia abajo). misma lista con valores en posiciones cambiadas.
def turn_down(array):
    cola = deque(array)
    cola.rotate(-3)
    return list(cola)

# funcion que rota el patron/cubo hacia la derecha.
# input: (patron). lista de 12 elementos con valores 1 y 0
# output: (patron rotado hacia abajo). misma lista con valores en posiciones cambiadas
def turn_right(array):
    return [array[11],array[2],array[8],array[5],array[3],array[6],array[4],array[1],array[7],array[10],array[0],array[9]]

# Comparacion entre nuestro patron y la lista de patrones.
# input: (lista_de_patrones, patron).
# lista_de_patrones: lista de listas con 18 elementos con valores 1 y 0.
# patron: lista de 18 elementos con valores 1 y 0
# output: True or False. True si patron esta presente en lista_de_patrones.
def check_cubes(big_arr,arr1):
    # arr1 in big_arr ::::::: remember to check time efficiency VS for
    for arr in big_arr:
        if (arr == arr1):
            return True
    return False

# funcion que rota el patron/cubo para ver si puede encontrar alguna coincidencia con el diccionario de patrones.
# input: (patron, diccionario)
# patron: lista de 12 elementos con valores 1 y 0
# diccionario: lista que contiene un conjunto de patrones en una lista, donde las llaves son la cantidad de nodos activos(valor 1)
# output: retorna el diccionario actualizado, este puede incluir o no el potencial patron dependiendo de si fue considerado valido o no.

def rotation_check(array, dict):
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
                if (check_cubes(ocurr_array,array)):
                    return dict
                array = turn_right(array)
            array = turn_down(array)
        # se rota el patron a la derecha, porque nos falta ver los lados de la izquierda y la derecha del patron,
        # como lados superiores e inferiores
        array = turn_right(array)
        for i in range(2):
            array = turn_down(array)
            for j in range(4):
                if (check_cubes(ocurr_array,array)):
                    return dict
                array = turn_right(array)
            array = turn_down(array)
    dict[counter].append(array)
    return dict

# PARTE LaTex -------------------------------------------------------------------------------


# funcion que traduce el patron, para ejemplificar en formato tikz.
# input: (patron).
# patron: lista de 12 elementos con valores 1 y 0.
# output: retorna un string que ejemplifica el patron que se desea mostrar.
def face_templates(array):
    faces = {}
    faces["front"] = array[0:4]
    faces["left"] = [array[11], array[2], array[8], array[5]] # array[2], array[5], array[8], array[11]
    faces["right"] = [array[10], array[7], array[1], array[4]] #array[1], array[4], array[7], array[10]
    faces["top"] = array[3:7]
    faces["back"] = [array[9], array[7], array[8], array[6]]
    faces["bottom"] = array[9:12] + array[0:1]
    # string que contiene la generacion del cubo en tikz.
    cube = """\draw[thick,fill=gray!20](3,3,0)--(0,3,0)--(0,3,3)--(3,3,3)--(3,3,0)--(3,0,0)--(3,0,3)--(0,0,3)--(0,3,3);
    \draw[thick](3,3,3)--(3,0,3);
    \draw[fill=gray!20](0,3,0)--(3,3,0)--(3,3,3)--(0,3,3)--(0,3,0);
    \draw[thick, densely dashed](3,0,0)--(0,0,0)--(0,3,0);
    \draw[thick, densely dashed](0,0,0)--(0,0,3);
"""
    for k,v in faces.items():
        nodos = v.count(1)
        if (nodos == 1):
            arreglonodos=[]
            # arreglos con las coordenadas base para el patron de 1 arista
            dosNabajo = [[1, 0, 0], [1, 2, 0], [2, 2, 0], [2, 0, 0], [0, 3, 0], [1, 2, 0], [3, 3, 0], [2, 2, 0]]
            dosNderecha = [[3, 1, 0], [1, 1, 0], [1, 2, 0], [3, 2, 0], [0, 0, 0], [1, 1, 0], [0, 3, 0], [1, 2, 0]]
            dosNarriba = [[1, 3, 0], [1, 1, 0], [2, 1, 0], [2, 3, 0], [0, 0, 0], [1, 1, 0], [3, 0, 0], [2, 1, 0]]
            dosNizquierda = [[0, 2, 0], [2, 2, 0], [2, 1, 0], [0, 1, 0], [2, 2, 0], [3, 3, 0], [2, 1, 0], [3, 0, 0]]
            if(v[0]==1):
                arreglonodos=terdimension(k,dosNabajo)
                if (k == "top"):
                    arreglonodos = terdimension(k,dosNarriba)
            elif(v[1]==1):
                if (k == "right"):
                    arreglonodos = terdimension(k, dosNizquierda)
                else:
                    arreglonodos=terdimension(k,dosNderecha)
            elif(v[3]==1):
                if (k== "top"):
                    arreglonodos = terdimension(k, dosNabajo)
                else:
                    arreglonodos=terdimension(k,dosNarriba)
            else:
                arreglonodos=terdimension(k,dosNizquierda)
            cube = translateDosNod(cube,arreglonodos,k)

        elif (nodos == 2 and v[0]!=v[3]):
            arreglo1 = []
            arreglo2 = []
            # coordenada base que contiene cualquier patron de 2 aristas adyacentes
            base = [[0,0,0],[1,1,0],[2,1,0],[3,0,0]  ,[0,3,0],[1,2,0],[2,2,0],[3,3,0] ,[1,1,0],[1,2,0] ,[2,2,0],[2,1,0]]
            # coordenadas especificas dada la posicion de los nodos en las aristas adyacentes.
            tresNizq = [[0, 1, 0], [0.7, 1.2, 0], [0.7, 1.8, 0], [0, 2, 0], [0.7, 1.2, 0], [1, 1, 0], [0.7, 1.8, 0],
                        [1, 2, 0]]
            tresNarriba = [[1, 3, 0], [1.2, 2.3, 0], [1.8, 2.3, 0], [2, 3, 0], [1.2, 2.3, 0], [1, 2, 0], [1.8, 2.3, 0],
                           [2, 2, 0]]
            tresNderecha = [[3, 1, 0], [2.3, 1.2, 0], [2.3, 1.8, 0], [3, 2, 0], [2.3, 1.2, 0], [2, 1, 0], [2.3, 1.8, 0],
                            [2, 2, 0]]
            tresNabajo = [[1, 0, 0], [1.2, 0.7, 0], [1.8, 0.7, 0], [2, 0, 0], [1.2, 0.7, 0], [1, 1, 0], [1.8, 0.7, 0],
                          [2, 1, 0]]
            if(v[0]==v[1]==1):
                terdimension(k,base)
                if (k=="top"):
                    arreglo1 = terdimension(k,tresNarriba)
                else:
                    arreglo1 =terdimension(k,tresNabajo)
                if (k=="right"):
                    arreglo2 = terdimension(k,tresNizq)
                else:
                    arreglo2 = terdimension(k,tresNderecha)
            elif(v[1]==v[3]==1):
                terdimension(k,base)
                if (k=="right"):
                    arreglo1 = terdimension(k,tresNizq)
                else:
                    arreglo1 =terdimension(k,tresNderecha)
                if (k=="top"):
                    arreglo2 = terdimension(k,tresNabajo)
                else:
                    arreglo2 = terdimension(k,tresNarriba)
            elif(v[3]==v[2]==1):
                terdimension(k,base)
                if (k=="top"):
                    arreglo1 = terdimension(k,tresNabajo)
                else:
                    arreglo1 =terdimension(k,tresNarriba)
                if (k=="right"):
                    arreglo2 = terdimension(k,tresNderecha)
                else:
                    arreglo2 = terdimension(k,tresNizq)
            elif(v[2]==v[0]==1):
                terdimension(k,base)
                if (k=="right"):
                    arreglo1 = terdimension(k,tresNderecha)
                else:
                    arreglo1 =terdimension(k,tresNizq)
                if (k=="top"):
                    arreglo2 = terdimension(k, tresNarriba)
                else:
                    arreglo2 = terdimension(k,tresNabajo)
            cube = translateTresNod(cube,base,arreglo1,arreglo2,k)
        elif (nodos == 4):
            arre = terdimension(k,[[0,1,0],[3,1,0], [0,2,0],[3,2,0], [1,0,0],[1,3,0], [2,0,0],[2,3,0]])
            cube = translateCuatroNod(cube,arre,k)
    return cube

# Seccion que se dedica a generar la cara como formato tikz --------------------------------------------------------------------

# funcion que redimensiona las coordenadas segun la posicion que representan
# input: (posicion, cara).
# posicion: posicion que representa la cara dentro en el cubo.
# cara: lista de x elementos que contiene las coordenadas para ejemplificar dicho patron.
# output: retorna un string que ejemplifica la cara en formato tikz.

def terdimension(posicion,array):
    if (posicion == "front"):
        for i in range(len(array)):
            array[i][2] += 3
    elif(posicion == "bottom" or posicion == "top"):
        for i in range(len(array)):
            array[i][2], array[i][1] = array[i][1], array[i][2]
            if (posicion == "top"):
                array[i][1] +=3
    elif(posicion == "left" or posicion == "right"):
        for i in range(len(array)):
            array[i][2], array[i][0] = array[i][0], array[i][2]
            if (posicion == "right"):
                array[i][0] += 3
    return array

# funcion que actualiza el string global con la informacion para representar dicha cara como tikz.
# input: (string,coordenadas,posicion).
# string: string global que se escribira en el documento para reproducir el patron en formato tikz.
# coordenadas: lista de x elementos que contiene las coordenadas para ejemplificar dicho la cara de dicho patron.
# posicion: posicion que representa la cara dentro en el cubo.
# output: retorna un string que ejemplifica la cara de una arista en formato tikz.

def translateDosNod(cube,array,k):
    options = "line width=0.4mm"
    if (k in ["left", "back", "bottom"]):
        options = "line width=0.4mm,gray,densely dashed"
    primera_linea = str(tuple(array[0]))+"--"+str(tuple(array[1]))+"--"+str(tuple(array[2]))+"--"+str(tuple(array[3]))+";"
    segunda_linea = str(tuple(array[4]))+"--"+str(tuple(array[5]))+";"
    tercera_linea = str(tuple(array[6]))+"--"+str(tuple(array[7]))+";"
    cube += """\draw["""+options+"""]"""+ primera_linea +"""
    \draw["""+options+"""]"""+segunda_linea+"""
    \draw["""+options+"""]"""+tercera_linea+"""
    """
    return cube

# funcion que actualiza el string global con la informacion para representar dicha cara como tikz.
# input: (string,base,fig1,fig2,posicion).
# string: string global que se escribira en el documento para reproducir el patron en formato tikz.
# base: lista de x elementos que contiene las coordenadas para ejemplificar la base de la cara de aristas adyacentes.
# fig1: lista con las coordenadas que detallan la seccion a dibujar en la cara(superior,inferior,derecha,izquierda).
# fig2: lista con las coordenadas que detallan la seccion a dibujar en la cara(superior,inferior,derecha,izquierda).
# posicion: posicion que representa la cara dentro en el cubo.
# output: retorna un string que ejemplifica la cara de aristas adyacentes en formato tikz.

def translateTresNod(cube,base,fig1,fig2,k):
    options = "line width=0.4mm"
    if (k in ["left", "back", "bottom"]):
        options = "line width=0.4mm,gray,densely dashed"
    primera_linea = str(tuple(base[0]))+"--"+str(tuple(base[1]))+"--"+str(tuple(base[2]))+"--"+str(tuple(base[3]))+";"
    segunda_linea = str(tuple(base[4])) + "--" + str(tuple(base[5])) + "--" + str(tuple(base[6])) + "--" + str(
        tuple(base[7])) + ";"
    tercera_linea = str(tuple(base[8]))+"--"+str(tuple(base[9]))+";"
    cuarta_linea = str(tuple(base[10]))+"--"+str(tuple(base[11]))+";"
    cube += """\draw["""+options+"""]"""+ primera_linea +"""
    \draw["""+options+"""]"""+segunda_linea+"""
    \draw["""+options+"""]"""+tercera_linea+"""
    \draw["""+options+"""]"""+cuarta_linea+"""
    """
    fig1_primera = str(tuple(fig1[0])) + "--" + str(tuple(fig1[1])) + "--" + str(tuple(fig1[2])) + "--" + str(tuple(fig1[3])) + ";"
    fig1_segunda = str(tuple(fig1[4])) + "--" + str(tuple(fig1[5])) + ";"
    fig1_tercera = str(tuple(fig1[6])) + "--" + str(tuple(fig1[7])) + ";"

    fig2_primera = str(tuple(fig2[0])) + "--" + str(tuple(fig2[1])) + "--" + str(tuple(fig2[2])) + "--" + str(tuple(fig2[3])) + ";"
    fig2_segunda = str(tuple(fig2[4])) + "--" + str(tuple(fig2[5])) + ";"
    fig2_tercera = str(tuple(fig2[6])) + "--" + str(tuple(fig2[7])) + ";"

    cube += """\draw["""+options+"""]""" + fig1_primera + """
        \draw["""+options+"""]""" + fig1_segunda + """
        \draw["""+options+"""]""" + fig1_tercera + """
        \draw["""+options+"""]""" + fig2_primera + """
        \draw["""+options+"""]""" + fig2_segunda + """
        \draw["""+options+"""]""" + fig2_tercera + """
        """
    return cube

# funcion que actualiza el string global con la informacion para representar dicha cara como tikz.
# input: (string,coordenadas,posicion).
# string: string global que se escribira en el documento para reproducir el patron en formato tikz.
# coordenadas: lista de x elementos que contiene las coordenadas para ejemplificar dicho la cara de dicho patron.
# posicion: posicion que representa la cara dentro en el cubo.
# output: retorna un string que ejemplifica la cara de 4 aristas en formato tikz.

def translateCuatroNod(cube,array,k):
    options = "line width=0.4mm"
    if (k in ["left", "back", "bottom"]):
        options = "line width=0.4mm,gray,densely dashed"
    primera_linea = str(tuple(array[0]))+"--"+str(tuple(array[1]))+";"
    segunda_linea = str(tuple(array[2]))+"--"+str(tuple(array[3]))+";"
    tercera_linea = str(tuple(array[4]))+"--"+str(tuple(array[5]))+";"
    cuarta_linea = str(tuple(array[6])) + "--" + str(tuple(array[7])) + ";"
    cube += """\draw["""+options+"""]"""+ primera_linea +"""
    \draw["""+options+"""]"""+segunda_linea+"""
    \draw["""+options+"""]"""+tercera_linea+"""
    \draw["""+options+"""]"""+cuarta_linea+"""
    """
    return cube



# En este codigo encontramos el total de patrones descrito por Ibanez, luego lo discriminamos de forma preliminar con los
# limites establecidos por Ito en su paper, esto lo reduce a 31 patrones en total.
# el total es 14, pero eso se reviso de forma manual con los resultados obtenidos por el script realizado TODO.
if __name__ == '__main__':
    start = time.time()
    # similar a los otros scripts, se genera un diccionario que contendra los potenciales patrones.
    dict = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: []}

    # genera todos los casos posibles para nodos activos, representando el cubo como una lista de 18 elementos.
    # los elementos representan los nodos activos ya sea como 1 = activo y 0 = no activo.
    # los primeros 12 elementos [0,...,11] representan las aristas del cubo, como se observa en el dibujo de la memoria.
    # el total de casos se puede sacar como 2^(repeat) en este caso es 2^18.
    casos = list(itertools.product([0, 1], repeat=12))
    print("length: ",len(casos))
    contador = 0
    for arr in casos:
        # chequeo y rotacion de los potenciales patrones con lo presentes en el diccionario
        rotation_check(list(arr), dict)
        contador+=1
        if (contador%10000 == 0):
            print("han ocurrido: "+str(contador)+" casos")
    total = 0
    validos = 0
    valid = []
    # chequeamos si los patrones son validos para las condiciones de ito de una forma preliminar.
    hash_validos = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
    for k,v in dict.items():
        total+=len(v)
        print(str(k)+ ": " + str(len(v)))
        for arr in v:
            if (face_validation(arr)):
                validos+=1
                hash_validos[arr.count(1)] +=1
                valid.append(arr)
    # print del total de posibles patrones unicos.
    print(total)
    # print del total de patrones segun nodos activos
    print(hash_validos)
    # reduccion del total de posibles patrones unicos.
    print(validos)
    # print de los patrones
    print(valid)
    # with open("results_ibanez.json", "w") as write_file:
    #     json.dump(valid, write_file)

    # genera un archivo de texto para copiar el contenido y copiarlo en un archivo LaTex utilizando tikz
    file1 = open("ibanez.txt", "w")
    cont = 1
    # genera patron para dibujar en tikz
    for arreglo in valid:
        inicio_string = """{\Large{Patron """ + str(cont) + """}}
            \par
            \\begin{minipage}{.45\linewidth}
                \\textbf{Nodos:}\n
                """
        file1.write(inicio_string)
        file1.write(str(arreglo))
        mid_string = """
                \end{minipage}\hfill
            \\begin{minipage}{.45\linewidth}
                \\begin{tikzpicture} \n
            """
        file1.write(mid_string)
        string = face_templates(arreglo)
        file1.write(string)
        cont += 1
        end_string = """
                \end{tikzpicture}
                \end{minipage}
                \par

            """
        file1.write(end_string)

    file1.close()
    end = time.time()

    print("Tiempo de ejecucion: ", (end-start))