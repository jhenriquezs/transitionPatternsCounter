import json


# funcion que traduce el patron, para ejemplificar en formato tikz.
# input: (patron).
# patron: lista de 12 elementos con valores 1 y 0.
# output: retorna un string que ejemplifica el patron que se desea mostrar.
def face_templates(array):
    faces = {}
    faces["front"] = array[0:4]
    faces["left"] = [array[6],array[0],array[4],array[2]]
    faces["right"] = [array[1],array[7],array[3],array[5]]
    faces["top"] = array[2:6]
    faces["back"] = [array[6],array[7],array[4],array[5]]
    faces["bottom"] = [array[6],array[7],array[0],array[1]]
    cube = """\draw[thick,fill=gray!20](3,3,0)--(0,3,0)--(0,3,3)--(3,3,3)--(3,3,0)--(3,0,0)--(3,0,3)--(0,0,3)--(0,3,3);
    \draw[thick](3,3,3)--(3,0,3);
    \draw[fill=gray!20](0,3,0)--(3,3,0)--(3,3,3)--(0,3,3)--(0,3,0);
    \draw[thick, densely dashed](3,0,0)--(0,0,0)--(0,3,0);
    \draw[thick, densely dashed](0,0,0)--(0,0,3);
"""
    for k,v in faces.items():
        nodos = v.count(1)
        if (nodos == 2 and (v[1] != v[2])):
            arreglonodos=[]
            # arreglos con las coordenadas base para el patron de 1 arista
            dosNabajo = [[1, 0, 0], [1, 2, 0], [2, 2, 0], [2, 0, 0], [0, 3, 0], [1, 2, 0], [3, 3, 0], [2, 2, 0]]
            dosNderecha = [[3, 1, 0], [1, 1, 0], [1, 2, 0], [3, 2, 0], [0, 0, 0], [1, 1, 0], [0, 3, 0], [1, 2, 0]]
            dosNarriba = [[1, 3, 0], [1, 1, 0], [2, 1, 0], [2, 3, 0], [0, 0, 0], [1, 1, 0], [3, 0, 0], [2, 1, 0]]
            dosNizquierda = [[0, 2, 0], [2, 2, 0], [2, 1, 0], [0, 1, 0], [2, 2, 0], [3, 3, 0], [2, 1, 0], [3, 0, 0]]
            if(v[0]==v[1] and v[0]==1):
                arreglonodos=terdimension(k,dosNabajo)
            elif(v[1]==v[3] and v[3]==1):
                if (k == "right"):
                    arreglonodos = terdimension(k, dosNizquierda)
                else:
                    arreglonodos=terdimension(k,dosNderecha)
            elif(v[3]==v[2] and v[2]==1):
                if (k== "top"):
                    arreglonodos = terdimension(k, dosNabajo)
                else:
                    arreglonodos=terdimension(k,dosNarriba)
            else:
                arreglonodos=terdimension(k,dosNizquierda)
            cube = translateDosNod(cube,arreglonodos,k)

        elif (nodos == 3):
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
            if(v[0]==v[1]==v[3]):
                terdimension(k,base)
                if (k=="top"):
                    arreglo1 = terdimension(k,tresNarriba)
                else:
                    arreglo1 =terdimension(k,tresNabajo)
                if (k=="right"):
                    arreglo2 = terdimension(k,tresNizq)
                else:
                    arreglo2 = terdimension(k,tresNderecha)
            elif(v[1]==v[3]==v[2]):
                terdimension(k,base)
                if (k=="right"):
                    arreglo1 = terdimension(k,tresNizq)
                else:
                    arreglo1 =terdimension(k,tresNderecha)
                if (k=="top"):
                    arreglo2 = terdimension(k,tresNabajo)
                else:
                    arreglo2 = terdimension(k,tresNarriba)
            elif(v[3]==v[2]==v[0]):
                terdimension(k,base)
                if (k=="top"):
                    arreglo1 = terdimension(k,tresNabajo)
                else:
                    arreglo1 =terdimension(k,tresNarriba)
                if (k=="right"):
                    arreglo2 = terdimension(k,tresNderecha)
                else:
                    arreglo2 = terdimension(k,tresNizq)
            elif(v[2]==v[0]==v[1]):
                terdimension(k,base)
                if (k=="right"):
                    arreglo1 = terdimension(k,tresNderecha)
                else:
                    arreglo1 =terdimension(k,tresNizq)
                if (k=="top"):
                    arreglo2 = terdimension(k, tresNarriba)
                else:
                    arreglo2 = terdimension(k,tresNabajo)
            print(v)
            cube = translateTresNod(cube,base,arreglo1,arreglo2,k)
        elif (nodos == 4):
            arre = terdimension(k,[[0,1,0],[3,1,0], [0,2,0],[3,2,0], [1,0,0],[1,3,0], [2,0,0],[2,3,0]])
            cube = translateCuatroNod(cube,arre,k)
    return cube

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
    print(fig1)
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


if __name__ == '__main__':
    # se abren los patrones obtenidos en ito.py
    with open('ito_patterns.json') as json_file:
        data = json.load(json_file)

    file1 = open("Patrones_ito.txt","w")
    cont = 1
    # genera patron para dibujar en tikz, se elimina el primer patron, porque equivale a un cubo sin refinamiento.
    for cubos in data[1:]:
        inicio_string = """{\Large{Patron """ + str(cont) + """}}
        \par
        \\begin{minipage}{.45\linewidth}
        \\textbf{Nodos:}
        """+str(cubos[1])+"""\par
            \\textbf{Caras:}\n
            """
        file1.write(inicio_string)
        for num in cubos[0]:
            if(num == "2 nodos"):
                file1.write("\\textbf{Arista (2 nodos)}\par\n")
            elif(num=="3 nodos"):
                file1.write("\\textbf{Aristas adyacentes (3 nodos)}\par\n")
            elif(num=="4 nodos"):
                file1.write("\\textbf{Cara (4 nodos)}\par\n")
        mid_string = """
            \end{minipage}\hfill
        \\begin{minipage}{.45\linewidth}
            \\begin{tikzpicture} \n
        """
        file1.write(mid_string)
        string = face_templates(cubos[1])
        # file1.write("Patron "+str(cont)+" cubo: "+str(cubos[1])+"\n ")
        file1.write(string)
        cont+=1
        end_string = """
            \end{tikzpicture}
            \end{minipage}
            \par
    
        """
        file1.write(end_string)
    file1.close()
